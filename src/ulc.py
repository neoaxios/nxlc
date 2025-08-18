#!/usr/bin/env python3
"""
Count lines of code in a directory, summarized by language type.
Includes source code, markdown documentation, and development scripts.
"""

import os
import sys
import argparse
import subprocess
import re
import shutil
import threading
import platform
import logging
import functools
from abc import ABC, abstractmethod
from pathlib import Path
from collections import defaultdict, OrderedDict
from typing import Dict, List, Tuple, Set, Optional, Any, Callable, TypeVar, Protocol, Generic
import fnmatch

# ============================================================================
# HIERARCHICAL IGNORE SUPPORT (INTEGRATED)
# ============================================================================

class PatternMatcher(Protocol):
    """Interface for pattern matching operations."""
    
    def process_ignore_file(self, path: Path) -> List[str]:
        """Parse an ignore file and return patterns."""
        ...
    
    def matches_patterns(self, path: Path, patterns: List[str]) -> bool:
        """Check if path matches any of the patterns."""
        ...


class CacheStrategy(ABC):
    """Abstract base for different caching strategies."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[bool]:
        """Retrieve cached value."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: bool) -> None:
        """Store value in cache."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear the cache."""
        pass


class LRUCacheStrategy(CacheStrategy):
    """Thread-safe Least Recently Used cache implementation."""
    
    def __init__(self, max_size: int = 1000):
        self.cache = OrderedDict()
        self.max_size = max_size
        self._lock = threading.RLock()  # Reentrant lock for thread safety
    
    def get(self, key: str) -> Optional[bool]:
        with self._lock:
            if key in self.cache:
                # Move to end (most recently used)
                self.cache.move_to_end(key)
                return self.cache[key]
            return None
    
    def set(self, key: str, value: bool) -> None:
        with self._lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            else:
                if len(self.cache) >= self.max_size:
                    # Remove least recently used
                    self.cache.popitem(last=False)
                self.cache[key] = value
    
    def clear(self) -> None:
        with self._lock:
            self.cache.clear()
    
    def size(self) -> int:
        """Get current cache size (thread-safe)."""
        with self._lock:
            return len(self.cache)


class IgnoreFileReader:
    """Reusable component for reading ignore files across different systems."""
    
    MAX_FILE_SIZE = 1024 * 1024  # 1MB default limit
    
    @staticmethod
    def read_ignore_file(path: Path, 
                        max_size: int = None,
                        encoding: str = 'utf-8') -> List[str]:
        """
        Read and parse an ignore file with safety checks.
        Can be reused for .gitignore, .dockerignore, .ulcignore, etc.
        """
        if max_size is None:
            max_size = IgnoreFileReader.MAX_FILE_SIZE
            
        if not path.exists():
            return []
        
        # Check file size
        try:
            file_size = path.stat().st_size
            if file_size > max_size:
                logging.warning(f"Ignore file too large (>{max_size} bytes): {path}")
                return []
        except (OSError, IOError) as e:
            logging.warning(f"Failed to stat ignore file {path}: {e}")
            return []
        
        patterns = []
        try:
            with open(path, 'r', encoding=encoding, errors='ignore') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if line and not line.startswith('#'):
                        patterns.append(line)
        except (OSError, IOError) as e:
            logging.warning(f"Failed to read ignore file {path}: {e}")
        
        return patterns


class IgnoreContext:
    """Manages ignore patterns at a specific directory level."""
    
    MAX_FILE_SIZE = 1024 * 1024  # 1MB limit for ignore files
    
    def __init__(self, 
                 directory: Path,
                 pattern_matcher: PatternMatcher,
                 parent_context: Optional['IgnoreContext'] = None,
                 cache_strategy: Optional[CacheStrategy] = None,
                 case_insensitive: Optional[bool] = None):
        # Validate inputs
        if not isinstance(directory, Path):
            raise TypeError(f"directory must be a Path object, got {type(directory)}")
        if not directory.exists():
            raise ValueError(f"Directory {directory} does not exist")
        if not directory.is_dir():
            raise ValueError(f"Path {directory} is not a directory")
        if not hasattr(pattern_matcher, 'process_ignore_file') or not hasattr(pattern_matcher, 'matches_patterns'):
            raise TypeError("pattern_matcher must implement PatternMatcher protocol")
        if parent_context is not None and not isinstance(parent_context, IgnoreContext):
            raise TypeError(f"parent_context must be an IgnoreContext or None, got {type(parent_context)}")
        if cache_strategy is not None and not isinstance(cache_strategy, CacheStrategy):
            raise TypeError(f"cache_strategy must be a CacheStrategy or None, got {type(cache_strategy)}")
        
        self.directory = directory.resolve()  # Use absolute path
        self.pattern_matcher = pattern_matcher
        self.parent = parent_context
        self.patterns = []  # Local patterns from this dir's .ulcignore
        self.cache = cache_strategy or LRUCacheStrategy()
        
        # Auto-detect case sensitivity if not specified
        if case_insensitive is None:
            self.case_insensitive = platform.system() == 'Windows'
        else:
            self.case_insensitive = bool(case_insensitive)
            
        self._load_patterns()
    
    def _load_patterns(self):
        """Load .ulcignore patterns from current directory."""
        ulcignore_path = self.directory / '.ulcignore'
        if ulcignore_path.exists():
            # Limit file size to prevent DoS
            try:
                if ulcignore_path.stat().st_size > self.MAX_FILE_SIZE:
                    logging.warning(f".ulcignore file too large (>1MB): {ulcignore_path}")
                    return
            except (OSError, IOError) as e:
                logging.warning(f"Failed to stat .ulcignore file {ulcignore_path}: {e}")
                return
            self.patterns = self.pattern_matcher.process_ignore_file(ulcignore_path)
    
    def should_ignore(self, path: Path) -> bool:
        """Check if path should be ignored based on current and parent patterns."""
        result, _ = self.should_ignore_with_context(path)
        return result
    
    def should_ignore_with_context(self, path: Path) -> Tuple[bool, Optional['IgnoreContext']]:
        """Check if path should be ignored and return the context that caused it.
        
        Returns:
            Tuple of (is_ignored, ignoring_context)
        """
        # Check if path is under this directory
        try:
            relative_path = path.relative_to(self.directory)
        except ValueError:
            # Path is not under this directory, check parent
            if self.parent:
                return self.parent.should_ignore_with_context(path)
            return False, None
        
        # Use POSIX path for consistent cache keys across platforms
        cache_key = relative_path.as_posix()
        if self.case_insensitive:
            cache_key = cache_key.lower()
        
        # Check cache first
        cached_result = self.cache.get(cache_key)
        if cached_result is not None:
            # For cached results, we don't know which context caused it
            # so we return self as the context
            return cached_result, self if cached_result else None
        
        # Check local patterns first (more specific)
        if self.pattern_matcher.matches_patterns(relative_path, self.patterns):
            self.cache.set(cache_key, True)
            return True, self
        
        # Then check parent patterns (less specific)
        if self.parent:
            parent_ignored, parent_context = self.parent.should_ignore_with_context(path)
            if parent_ignored:
                self.cache.set(cache_key, True)
                return True, parent_context
        
        self.cache.set(cache_key, False)
        return False, None


class IgnoreContextFactory:
    """Factory for creating IgnoreContext instances with consistent configuration."""
    
    def __init__(self, 
                 pattern_matcher: PatternMatcher,
                 cache_strategy_factory: Callable[[], CacheStrategy] = None,
                 case_insensitive: Optional[bool] = None):
        self.pattern_matcher = pattern_matcher
        self.cache_strategy_factory = cache_strategy_factory or LRUCacheStrategy
        self.case_insensitive = case_insensitive
    
    def create_context(self, 
                      directory: Path, 
                      parent: Optional[IgnoreContext] = None) -> Optional[IgnoreContext]:
        """Create context only if .ulcignore exists (performance optimization)."""
        ulcignore_path = directory / '.ulcignore'
        if not ulcignore_path.exists() and parent is None:
            return None
        
        return IgnoreContext(
            directory=directory,
            pattern_matcher=self.pattern_matcher,
            parent_context=parent,
            cache_strategy=self.cache_strategy_factory(),
            case_insensitive=self.case_insensitive
        )


class LineCounterPatternAdapter:
    """Adapter to make LineCounter compatible with PatternMatcher interface."""
    
    def __init__(self, line_counter):
        """
        Initialize adapter with a LineCounter instance.
        
        Args:
            line_counter: Instance of LineCounter class
        """
        self.line_counter = line_counter
        self.file_reader = IgnoreFileReader()
    
    def process_ignore_file(self, path: Path) -> List[str]:
        """Parse an ignore file using shared reader."""
        return self.file_reader.read_ignore_file(path)
    
    def matches_patterns(self, path: Path, patterns: List[str]) -> bool:
        """Check if path matches patterns using LineCounter logic."""
        return self.line_counter.is_ulcignored(path, patterns)


# Generic type for future enhancements
T = TypeVar('T')  # Config type

class HierarchicalConfigContext(Generic[T]):
    """
    Generic hierarchical configuration context.
    Can be reused for any hierarchical config system.
    """
    
    def __init__(self,
                 directory: Path,
                 config_filename: str,
                 parser: Callable[[Path], T],
                 merger: Callable[[T, T], T],
                 parent: Optional['HierarchicalConfigContext[T]'] = None):
        self.directory = directory
        self.config_filename = config_filename
        self.parser = parser
        self.merger = merger
        self.parent = parent
        self.config = self._load_config()
    
    def _load_config(self) -> Optional[T]:
        """Load configuration from current directory."""
        config_path = self.directory / self.config_filename
        if config_path.exists():
            return self.parser(config_path)
        return None
    
    def get_effective_config(self) -> Optional[T]:
        """Get merged configuration from hierarchy."""
        local_config = self.config
        
        if self.parent:
            parent_config = self.parent.get_effective_config()
            if parent_config and local_config:
                return self.merger(parent_config, local_config)
            return local_config or parent_config
        
        return local_config

# Hierarchical support is now always available (integrated directly)

# ============================================================================
# CONFIGURATION AND LANGUAGE DEFINITIONS
# ============================================================================

class LanguageDefinitions:
    """Centralized language definitions and configuration."""
    
    # Configuration constants
    MAX_CACHE_SIZE = 10000
    
    # Directories to ignore
    IGNORE_DIRS = {
        '.git', '.svn', '.hg', '.bzr', '_darcs',
        'node_modules', '__pycache__', '.pytest_cache',
        'venv', '.venv', 'env', '.env', 'virtualenv',
        'dist', 'build', 'target', 'bin', 'obj',
        '.idea', '.vscode', '.vs',
        'coverage', 'htmlcov', '.coverage',
        '.tis', '.mypy_cache', '.ruff_cache',
        'mock_vitest',  # TIScore specific
    }
    
    # Extensions that have conflicts requiring content analysis
    CONFLICT_EXTENSIONS = {'.h', '.m', '.r', '.pl'}
    
    # Default language for conflicted extensions (fallback)
    EXTENSION_DEFAULTS = {
        '.h': 'C',          # Most common
        '.m': 'Objective-C', # MATLAB usually in matlab/ dirs
        '.r': 'R',          # R more common than Rebol
        '.pl': 'Perl',      # Perl more common than Prolog
    }
    
    # Shebang patterns for script detection
    SHEBANG_PATTERNS = {
        'python': 'Python',
        'perl': 'Perl', 
        'ruby': 'Ruby',
        'bash': 'Shell',
        'sh': 'Shell',
        'zsh': 'Shell',
        'fish': 'Shell',
        'node': 'JavaScript',
        'php': 'PHP',
        'lua': 'Lua',
    }
    
    # Language extensions mapping (moved from global scope)
    LANGUAGE_EXTENSIONS = {
        'Python': ['.py', '.pyw', '.pyx', '.pxd', '.pxi'],
        'JavaScript': ['.js', '.jsx', '.mjs', '.cjs'],
        'TypeScript': ['.ts', '.tsx', '.mts', '.cts'],
        'Vue': ['.vue'],
        'Svelte': ['.svelte'],
        'Java': ['.java'],
        'C': ['.c', '.h'],
        'C++': ['.cpp', '.cc', '.cxx', '.hpp', '.hxx', '.h++'],
        'C#': ['.cs'],
        'Go': ['.go'],
        'Rust': ['.rs'],
        'Ruby': ['.rb', '.erb'],
        'PHP': ['.php', '.php3', '.php4', '.php5', '.phtml'],
        'Swift': ['.swift'],
        'Kotlin': ['.kt', '.kts'],
        'Scala': ['.scala'],
        'Dart': ['.dart'],
        'R': ['.r', '.R', '.Rmd'],
        'Julia': ['.jl'],
        'Shell': ['.sh', '.bash', '.zsh', '.fish', '.ksh'],
        'PowerShell': ['.ps1', '.psm1', '.psd1'],
        'SQL': ['.sql'],
        'HTML': ['.html', '.htm', '.xhtml'],
        'CSS': ['.css', '.scss', '.sass', '.less'],
        'Markdown': ['.md', '.markdown', '.mdown', '.mkd'],
        'YAML': ['.yaml', '.yml'],
        'JSON': ['.json', '.jsonc'],
        'XML': ['.xml', '.xsl', '.xslt'],
        'TOML': ['.toml'],
        'Makefile': ['Makefile', 'makefile', 'GNUmakefile', '.mk'],
        'Dockerfile': ['Dockerfile', '.dockerfile'],
        'Configuration': ['.conf', '.config', '.cfg', '.ini', '.env'],
        'Text': ['.txt', '.text'],
        'README': ['README', 'README.txt', 'README.md', 'README.rst'],
        'Perl': ['.pl', '.pm', '.t'],
        'Lua': ['.lua'],
        'Haskell': ['.hs', '.lhs'],
        'Elixir': ['.ex', '.exs'],
        'Clojure': ['.clj', '.cljs', '.cljc'],
        'F#': ['.fs', '.fsx', '.fsi'],
        'Erlang': ['.erl', '.hrl'],
        'Zig': ['.zig'],
        'Nim': ['.nim', '.nims'],
        'Crystal': ['.cr'],
        # Database Languages
        'PL/SQL': ['.sql', '.pls', '.plb', '.pck', '.pkb', '.pks'],
        'CQL': ['.cql'],
        'HiveQL': ['.hql', '.q'],
        'Neo4j Cypher': ['.cypher'],
        # Legacy Languages
        'COBOL': ['.cob', '.cbl', '.cpy', '.ccp'],
        'FORTRAN': ['.f', '.for', '.f77', '.f90', '.f95', '.f03', '.f08'],
        'Pascal': ['.pas', '.pp', '.inc'],
        'Ada': ['.ada', '.adb', '.ads'],
        'Modula-2': ['.mod', '.def'],
        'Modula-3': ['.m3', '.i3'],
        'Oberon': ['.ob', '.ob2'],
        'ALGOL': ['.alg', '.a68'],
        'PL/I': ['.pli', '.pl1'],
        'RPG': ['.rpg', '.rpgle', '.sqlrpgle'],
        'JCL': ['.jcl', '.job'],
        'REXX': ['.rexx', '.rex'],
        'Assembly': ['.asm', '.s', '.S'],
        'BASIC': ['.bas', '.basic'],
        'Visual Basic': ['.vb'],
        # Domain-Specific Languages
        'Verilog': ['.v', '.vh'],
        'VHDL': ['.vhd', '.vhdl'],
        'SystemVerilog': ['.sv', '.svh'],
        'SPICE': ['.sp', '.spice', '.cir'],
        'AutoLISP': ['.lsp'],
        'TCL': ['.tcl', '.tk'],
        'Octave': ['.m'],
        'Mathematica': ['.nb', '.wl'],
        'Maple': ['.mpl', '.maple'],
        'Stata': ['.do', '.ado'],
        'SAS': ['.sas'],
        'SPSS': ['.sps'],
        'GDScript': ['.gd'],
        'UnrealScript': ['.uc'],
        'Linden Script': ['.lsl'],
        'OpenSCAD': ['.scad'],
        'PostScript': ['.ps', '.eps'],
        'TeX': ['.tex'],
        'BibTeX': ['.bib'],
        'Gnuplot': ['.gp', '.plt'],
        'DOT': ['.dot', '.gv'],
        'PlantUML': ['.puml', '.plantuml'],
        'Mermaid': ['.mmd', '.mermaid'],
        'Protocol Buffers': ['.proto'],
        'Thrift': ['.thrift'],
        'Avro': ['.avsc', '.avdl'],
        # Configuration & Markup Languages
        'INI': ['.ini', '.cfg'],
        'Properties': ['.properties'],
        'Plist': ['.plist'],
        'AsciiDoc': ['.adoc', '.asciidoc'],
        'ReStructuredText': ['.rst', '.rest'],
        'Org Mode': ['.org'],
        'MediaWiki': ['.wiki', '.mediawiki'],
        'Textile': ['.textile'],
        'Creole': ['.creole'],
        'HAML': ['.haml'],
        'Slim': ['.slim'],
        'Pug': ['.pug', '.jade'],
        'Handlebars': ['.hbs', '.handlebars'],
        'Mustache': ['.mustache'],
        'Jinja2': ['.j2', '.jinja', '.jinja2'],
        'Liquid': ['.liquid'],
        'Smarty': ['.tpl'],
        'Twig': ['.twig'],
        'ERB': ['.erb', '.rhtml'],
        'XAML': ['.xaml'],
        'QML': ['.qml'],
        'Glade': ['.glade'],
        'SVG': ['.svg'],
        'KML': ['.kml'],
        'RSS': ['.rss'],
        'Atom': ['.atom'],
        'OPML': ['.opml'],
        'RDF': ['.rdf', '.owl'],
        'WSDL': ['.wsdl'],
        'XSD': ['.xsd'],
    }
    
    # Comment patterns for different languages
    COMMENT_PATTERNS = {
        'Python': {'single': ['#'], 'multi_start': ['"""', "'''"], 'multi_end': ['"""', "'''"]},
        'JavaScript': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'TypeScript': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Java': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'C': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'C++': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'C#': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Go': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Rust': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Ruby': {'single': ['#'], 'multi_start': ['=begin'], 'multi_end': ['=end']},
        'PHP': {'single': ['//', '#'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Swift': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Kotlin': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Shell': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'PowerShell': {'single': ['#'], 'multi_start': ['<#'], 'multi_end': ['#>']},
        'SQL': {'single': ['--'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'HTML': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'CSS': {'single': [], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'XML': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'YAML': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'JSON': {'single': [], 'multi_start': [], 'multi_end': []},  # JSON doesn't have comments
        'TOML': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Makefile': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Dockerfile': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Configuration': {'single': ['#', ';', '//'], 'multi_start': [], 'multi_end': []},
        'Perl': {'single': ['#'], 'multi_start': ['=pod'], 'multi_end': ['=cut']},
        'Lua': {'single': ['--'], 'multi_start': ['--[['], 'multi_end': [']]']},
        'Haskell': {'single': ['--'], 'multi_start': ['{-'], 'multi_end': ['-}']},
        'Elixir': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Clojure': {'single': [';'], 'multi_start': [], 'multi_end': []},
        'F#': {'single': ['//'], 'multi_start': ['(*'], 'multi_end': ['*)']},
        'Erlang': {'single': ['%'], 'multi_start': [], 'multi_end': []},
        'Zig': {'single': ['//'], 'multi_start': [], 'multi_end': []},
        'Nim': {'single': ['#'], 'multi_start': ['#['], 'multi_end': [']#']},
        'Crystal': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Scala': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Dart': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'R': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Julia': {'single': ['#'], 'multi_start': ['#='], 'multi_end': ['=#']},
        'Vue': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'Svelte': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        # Legacy Languages
        'COBOL': {'single': ['*'], 'multi_start': [], 'multi_end': []},  # In column 7
        'FORTRAN': {'single': ['!', 'C', 'c'], 'multi_start': [], 'multi_end': []},
        'Pascal': {'single': ['//'], 'multi_start': ['{', '(*'], 'multi_end': ['}', '*)']},
        'Ada': {'single': ['--'], 'multi_start': [], 'multi_end': []},
        'Modula-2': {'single': [], 'multi_start': ['(*'], 'multi_end': ['*)']},
        'Modula-3': {'single': [], 'multi_start': ['(*'], 'multi_end': ['*)']},
        'Oberon': {'single': [], 'multi_start': ['(*'], 'multi_end': ['*)']},
        'ALGOL': {'single': [], 'multi_start': ['comment'], 'multi_end': [';']},
        'PL/I': {'single': [], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'RPG': {'single': ['*'], 'multi_start': [], 'multi_end': []},
        'JCL': {'single': ['//*'], 'multi_start': [], 'multi_end': []},
        'REXX': {'single': [], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Assembly': {'single': [';', '#', '//'], 'multi_start': [], 'multi_end': []},
        'BASIC': {'single': ["'", 'REM'], 'multi_start': [], 'multi_end': []},
        'Visual Basic': {'single': ["'"], 'multi_start': [], 'multi_end': []},
        # Database Languages
        'PL/SQL': {'single': ['--'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'CQL': {'single': ['--'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'HiveQL': {'single': ['--'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Neo4j Cypher': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        # Domain-Specific Languages
        'Verilog': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'VHDL': {'single': ['--'], 'multi_start': [], 'multi_end': []},
        'SystemVerilog': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'SPICE': {'single': ['*'], 'multi_start': [], 'multi_end': []},
        'AutoLISP': {'single': [';'], 'multi_start': [], 'multi_end': []},
        'TCL': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Octave': {'single': ['#', '%'], 'multi_start': ['%{'], 'multi_end': ['%}']},
        'Mathematica': {'single': [], 'multi_start': ['(*'], 'multi_end': ['*)']},
        'Maple': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'Stata': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'SAS': {'single': ['*'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'SPSS': {'single': ['*'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'GDScript': {'single': ['#'], 'multi_start': ['"""'], 'multi_end': ['"""']},
        'UnrealScript': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Linden Script': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'OpenSCAD': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'PostScript': {'single': ['%'], 'multi_start': [], 'multi_end': []},
        'TeX': {'single': ['%'], 'multi_start': [], 'multi_end': []},
        'BibTeX': {'single': ['%'], 'multi_start': [], 'multi_end': []},
        'Gnuplot': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'DOT': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'PlantUML': {'single': ["'"], 'multi_start': ["/'"], 'multi_end': ["'/"]},
        'Mermaid': {'single': ['%%'], 'multi_start': [], 'multi_end': []},
        'Protocol Buffers': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Thrift': {'single': ['#', '//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Avro': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        # Configuration & Markup Languages
        'INI': {'single': [';', '#'], 'multi_start': [], 'multi_end': []},
        'Properties': {'single': ['#', '!'], 'multi_start': [], 'multi_end': []},
        'Plist': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'AsciiDoc': {'single': ['//'], 'multi_start': ['////'], 'multi_end': ['////']},
        'ReStructuredText': {'single': ['..'], 'multi_start': [], 'multi_end': []},
        'Org Mode': {'single': ['#'], 'multi_start': [], 'multi_end': []},
        'MediaWiki': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'Textile': {'single': [], 'multi_start': ['###.'], 'multi_end': ['###.']},
        'Creole': {'single': [], 'multi_start': [], 'multi_end': []},
        'HAML': {'single': ['-#'], 'multi_start': [], 'multi_end': []},
        'Slim': {'single': ['/'], 'multi_start': [], 'multi_end': []},
        'Pug': {'single': ['//'], 'multi_start': [], 'multi_end': []},
        'Handlebars': {'single': [], 'multi_start': ['{{!'], 'multi_end': ['}}']},
        'Mustache': {'single': [], 'multi_start': ['{{!'], 'multi_end': ['}}']},
        'Jinja2': {'single': [], 'multi_start': ['{#'], 'multi_end': ['#}']},
        'Liquid': {'single': [], 'multi_start': ['{% comment %}'], 'multi_end': ['{% endcomment %}']},
        'Smarty': {'single': [], 'multi_start': ['{*'], 'multi_end': ['*}']},
        'Twig': {'single': [], 'multi_start': ['{#'], 'multi_end': ['#}']},
        'ERB': {'single': [], 'multi_start': ['<%#'], 'multi_end': ['%>']},
        'XAML': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'QML': {'single': ['//'], 'multi_start': ['/*'], 'multi_end': ['*/']},
        'Glade': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'SVG': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'KML': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'RSS': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'Atom': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'OPML': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'RDF': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'WSDL': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
        'XSD': {'single': [], 'multi_start': ['<!--'], 'multi_end': ['-->']},
    }


# ============================================================================
# PLATFORM ADAPTERS
# ============================================================================

class PlatformAdapter(ABC):
    """Abstract base class for platform-specific adaptations."""
    
    @abstractmethod
    def get_platform_name(self) -> str:
        """Get the platform name."""
        pass
    
    @abstractmethod
    def is_executable(self, path: Path) -> bool:
        """Check if a file is executable on this platform."""
        pass
    
    @abstractmethod
    def normalize_path(self, path: Path) -> Path:
        """Normalize path for this platform."""
        pass


class UnixAdapter(PlatformAdapter):
    """Unix/Linux platform adapter."""
    
    def get_platform_name(self) -> str:
        return "Unix"
    
    def is_executable(self, path: Path) -> bool:
        return os.access(path, os.X_OK)
    
    def normalize_path(self, path: Path) -> Path:
        return path.resolve()


class WindowsAdapter(PlatformAdapter):
    """Windows platform adapter."""
    
    def get_platform_name(self) -> str:
        return "Windows"
    
    def is_executable(self, path: Path) -> bool:
        return path.suffix.lower() in {'.exe', '.bat', '.cmd', '.com'}
    
    def normalize_path(self, path: Path) -> Path:
        return path.resolve()


class MacAdapter(UnixAdapter):
    """macOS platform adapter (inherits from Unix)."""
    
    def get_platform_name(self) -> str:
        return "macOS"


def get_platform_adapter() -> PlatformAdapter:
    """Get the appropriate platform adapter for the current system."""
    system = platform.system()
    if system == "Windows":
        return WindowsAdapter()
    elif system == "Darwin":
        return MacAdapter()
    else:  # Linux and other Unix-like systems
        return UnixAdapter()


# ============================================================================
# SECURITY UTILITIES
# ============================================================================

def validate_linguist_path(path: str) -> bool:
    """Validate that the provided linguist path is safe and executable. Prevents command injection."""
    import string
    
    if not path or not isinstance(path, str):
        raise ValueError("Linguist path must be a non-empty string")
    
    # Prevent command injection - only allow safe characters
    safe_chars = string.ascii_letters + string.digits + '._-/\\'
    if not all(c in safe_chars for c in path):
        raise ValueError(f"Linguist path contains unsafe characters: {path}")
    
    # Prevent shell metacharacters
    dangerous_chars = ['&', '|', ';', '$', '`', '(', ')', '<', '>', '"', "'"]
    if any(char in path for char in dangerous_chars):
        raise ValueError(f"Linguist path contains shell metacharacters: {path}")
    
    # Must be an absolute path
    if not os.path.isabs(path):
        raise ValueError(f"Linguist path must be absolute: {path}")
    
    return True


def detect_file_encoding(filepath: Path) -> str:
    """Detect file encoding using multiple strategies."""
    try:
        # Try to import chardet for accurate detection
        import chardet
        with open(filepath, 'rb') as f:
            raw_data = f.read(min(32768, os.path.getsize(filepath)))
            result = chardet.detect(raw_data)
            if result['encoding'] and result['confidence'] > 0.7:
                return result['encoding']
    except (ImportError, OSError, IOError):
        pass
    
    # Fallback: Try common encodings
    common_encodings = ['utf-8', 'utf-16', 'iso-8859-1', 'cp1252']
    
    for encoding in common_encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                # Read a small sample to test encoding
                f.read(1024)
                return encoding
        except (UnicodeDecodeError, UnicodeError):
            continue
    
    # Final fallback
    return 'utf-8'


# ============================================================================
# UTILITY DECORATORS AND HELPERS  
# ============================================================================

F = TypeVar('F', bound=Callable[..., Any])

def handle_file_errors(default_return=None, log_errors=True):
    """Decorator for handling common file operation errors."""
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (OSError, IOError, UnicodeDecodeError, UnicodeError) as e:
                if log_errors and logging.getLogger().isEnabledFor(logging.WARNING):
                    logging.warning(f"File operation failed in {func.__name__}: {e}")
                return default_return
            except PermissionError as e:
                if log_errors and logging.getLogger().isEnabledFor(logging.WARNING):
                    logging.warning(f"Permission denied in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator


# ============================================================================
# LINE COUNTER CLASS
# ============================================================================

class LineCounter:
    """Universal Language Counter - Main class for counting lines of code with encapsulated state."""
    
    def __init__(self, platform_adapter=None, use_comprehensive=False, linguist_cmd=None, 
                 logger=None, colors=None):
        """Initialize LineCounter with configuration."""
        self.platform = platform_adapter or get_platform_adapter()
        self.use_comprehensive = use_comprehensive
        self.linguist_cmd = linguist_cmd
        self.linguist_lock = threading.Lock()
        self.language_defs = LanguageDefinitions()
        self.file_line_counts = {}
        self.logger = logger or logging.getLogger(__name__)
        self.colors = colors or Colors(enabled=True)
        
        # Validate linguist path if provided
        if linguist_cmd:
            validate_linguist_path(linguist_cmd)
    
    def _safe_open_file(self, filepath: Path):
        """Safely open file with proper encoding detection and error handling."""
        encoding = detect_file_encoding(filepath)
        return open(filepath, 'r', encoding=encoding, errors='ignore')
    
    def detect_language(self, filepath: Path) -> str:
        """Detect the programming language of a file."""
        # Handle special filenames first
        filename = filepath.name
        
        # Handle Makefiles
        if filename in {'Makefile', 'makefile', 'GNUmakefile'} or filename.endswith('.mk'):
            return 'Makefile'
        
        # Handle Dockerfiles
        if filename in {'Dockerfile'} or filename.endswith('.dockerfile'):
            return 'Dockerfile'
        
        # Handle READMEs
        if filename.upper().startswith('README'):
            return 'README'
        
        # Handle configuration files (including git config)
        if filename in {'.gitignore', '.gitattributes', '.gitmodules', '.dockerignore', '.npmignore'} or filename.endswith('.example'):
            return 'Configuration'
        
        # Get file extension
        if filepath.suffix:
            ext = filepath.suffix.lower()
        else:
            # Handle files without extensions by checking shebang first
            shebang_lang = self._detect_from_shebang(filepath)
            if shebang_lang != 'Unknown':
                return shebang_lang
            
            # If no shebang, check for common extensionless file types
            if filename.lower() in {'license', 'copying', 'authors', 'contributors', 'changelog', 'news', 'install', 'readme'}:
                return 'Text'
            
            return 'Unknown'
        
        # Handle conflicted extensions with content analysis
        if ext in self.language_defs.CONFLICT_EXTENSIONS:
            return self._resolve_conflict(filepath, ext)
        
        # Standard extension lookup
        for language, extensions in self.language_defs.LANGUAGE_EXTENSIONS.items():
            if ext in [e.lower() for e in extensions]:
                return language
        
        # Check for shebang if no extension match
        shebang_lang = self._detect_from_shebang(filepath)
        if shebang_lang != 'Unknown':
            return shebang_lang
        
        return 'Unknown'
    
    @handle_file_errors(default_return='Unknown', log_errors=True)
    def _detect_from_shebang(self, filepath: Path) -> str:
        """Detect language from shebang line."""
        with self._safe_open_file(filepath) as f:
            first_line = f.readline().strip()
            if first_line.startswith('#!'):
                for pattern, language in self.language_defs.SHEBANG_PATTERNS.items():
                    if pattern in first_line.lower():
                        return language
        return 'Unknown'
    
    @handle_file_errors(default_return=None, log_errors=True)
    def _resolve_conflict(self, filepath: Path, ext: str) -> str:
        """Resolve conflicted file extensions using content analysis."""
        with self._safe_open_file(filepath) as f:
            content = f.read(1000)  # Read first 1KB for analysis
            
            if ext == '.h':
                # C++ indicators
                if any(keyword in content for keyword in ['class ', 'template<', 'namespace ', 'std::', 'cout', 'cin']):
                    return 'C++'
                # Objective-C indicators
                elif any(keyword in content for keyword in ['@interface', '@implementation', '@property', 'NSString']):
                    return 'Objective-C'
                else:
                    return 'C'  # Default fallback
            
            elif ext == '.m':
                # MATLAB indicators
                if any(keyword in content for keyword in ['function ', 'end\n', 'fprintf', 'disp(']):
                    return 'MATLAB'
                # Objective-C indicators
                elif any(keyword in content for keyword in ['@interface', '@implementation', '@property', '#import']):
                    return 'Objective-C'
                else:
                    return self.language_defs.EXTENSION_DEFAULTS[ext]
            
            elif ext == '.r':
                # R indicators
                if any(keyword in content for keyword in ['library(', 'data.frame', '<-', 'ggplot']):
                    return 'R'
                else:
                    return 'Rebol'
            
            elif ext == '.pl':
                # Perl indicators
                if any(keyword in content for keyword in ['use strict', 'my $', 'print ', '#!/usr/bin/perl']):
                    return 'Perl'
                # Prolog indicators
                elif any(keyword in content for keyword in [':-', '?-', 'append([', 'member(']):
                    return 'Prolog'
                else:
                    return self.language_defs.EXTENSION_DEFAULTS[ext]
        
        # Return default if file operation failed
        return self.language_defs.EXTENSION_DEFAULTS.get(ext, 'Unknown')
    
    @handle_file_errors(default_return=(0, 0, 0), log_errors=True)
    def count_lines_in_file(self, filepath: Path) -> Tuple[int, int, int]:
        """Count lines in a single file. Returns (total, code, comment) lines."""
        language = self.detect_language(filepath)
        
        with self._safe_open_file(filepath) as f:
            lines = f.readlines()
        
        total_lines = len(lines)
        if total_lines == 0:
            return (0, 0, 0)
        
        # Get comment patterns for this language
        comment_patterns = self.language_defs.COMMENT_PATTERNS.get(language, {
            'single': [], 'multi_start': [], 'multi_end': []
        })
        
        code_lines = 0
        comment_lines = 0
        in_multiline_comment = False
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                continue
            
            is_comment = False
            
            # Handle multiline comments with proper state management
            # For Python: """ and ''' can both start and end multiline comments
            line_after_processing = stripped
            
            # Process multiline comment markers in the line
            for start_pattern in comment_patterns['multi_start']:
                if start_pattern in line_after_processing:
                    # Count occurrences of the pattern
                    pattern_count = line_after_processing.count(start_pattern)
                    
                    if in_multiline_comment:
                        # We're in a multiline comment, look for end
                        if pattern_count % 2 == 1:
                            # Odd number of patterns - ends the multiline comment
                            in_multiline_comment = False
                        # Even number (including 0) - stays in multiline comment
                        is_comment = True
                    else:
                        # We're not in a multiline comment, look for start
                        if pattern_count % 2 == 1:
                            # Odd number of patterns - starts a multiline comment
                            in_multiline_comment = True
                        is_comment = True
                    break  # Only process the first matching pattern
            
            # If not handled by multiline logic, check for single-line comments
            if not is_comment and not in_multiline_comment:
                for comment_prefix in comment_patterns['single']:
                    if stripped.startswith(comment_prefix):
                        is_comment = True
                        break
            
            # If we're in a multiline comment and no end was found, it's a comment
            if in_multiline_comment and not is_comment:
                is_comment = True
            
            if is_comment:
                comment_lines += 1
            else:
                code_lines += 1
        
        return (total_lines, code_lines, comment_lines)
    
    def should_ignore_directory(self, dir_path: Path) -> bool:
        """Check if a directory should be ignored."""
        return dir_path.name in self.language_defs.IGNORE_DIRS
    
    def should_ignore_file(self, file_path: Path) -> bool:
        """Check if a file should be ignored."""
        # Skip very large files (>10MB)
        try:
            if file_path.stat().st_size > 10 * 1024 * 1024:
                return True
        except OSError:
            return True
        
        # Skip binary files by extension
        binary_extensions = {
            '.pyc', '.pyo', '.class', '.jar', '.war', '.ear',
            '.exe', '.dll', '.so', '.dylib', '.a', '.lib',
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico',
            '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
            '.zip', '.tar', '.gz', '.bz2', '.7z', '.rar',
            '.mp3', '.mp4', '.avi', '.mov', '.wmv', '.flv',
            '.db', '.sqlite', '.sqlite3'
        }
        
        if file_path.suffix.lower() in binary_extensions:
            return True
        
        return False
    
    def is_git_repository(self, directory: Path) -> bool:
        """Check if directory is a git repository."""
        git_dir = directory / '.git'
        return git_dir.exists() and (git_dir.is_dir() or git_dir.is_file())
    
    @handle_file_errors(default_return=[], log_errors=True)
    def process_gitignore(self, gitignore_path: Path) -> List[str]:
        """Process .gitignore file and return list of patterns."""
        patterns = []
        with self._safe_open_file(gitignore_path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    patterns.append(line)
        return patterns
    
    @handle_file_errors(default_return=[], log_errors=True)
    def process_ulcignore(self, ulcignore_path: Path) -> List[str]:
        """Process .ulcignore file and return list of patterns."""
        patterns = []
        with self._safe_open_file(ulcignore_path) as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if line and not line.startswith('#'):
                    patterns.append(line)
        return patterns
    
    def is_gitignored(self, file_path: Path, git_patterns: List[str]) -> bool:
        """Check if a file matches any gitignore pattern."""
        for pattern in git_patterns:
            if fnmatch.fnmatch(str(file_path), pattern) or fnmatch.fnmatch(file_path.name, pattern):
                return True
        return False
    
    def is_ulcignored(self, file_path: Path, ulc_patterns: List[str]) -> bool:
        """Check if a file or directory matches any ulcignore pattern.
        
        Supports negation patterns (!) to re-include previously excluded files.
        Patterns are evaluated in order, with later patterns overriding earlier ones.
        """
        path_str = str(file_path).replace('\\', '/')  # Normalize for cross-platform
        is_ignored = False
        
        for pattern in ulc_patterns:
            # Normalize pattern for cross-platform
            pattern = pattern.replace('\\', '/')
            
            # Handle negation patterns
            if pattern.startswith('!'):
                # Remove the ! and check if the remaining pattern matches
                negated_pattern = pattern[1:]
                if self._matches_single_pattern(file_path, path_str, negated_pattern):
                    is_ignored = False  # Re-include the file
            else:
                # Regular pattern - check if it matches
                if self._matches_single_pattern(file_path, path_str, pattern):
                    is_ignored = True  # Exclude the file
        
        return is_ignored
    
    def _matches_single_pattern(self, file_path: Path, path_str: str, pattern: str) -> bool:
        """Check if a path matches a single pattern."""
        # Handle ** patterns (match anywhere in path)
        if '**/' in pattern:
            # Pattern like **/test_data/ should match test_data anywhere
            if pattern.startswith('**/') and pattern.endswith('/'):
                # Directory pattern: **/dirname/
                dir_name = pattern[3:-1]
                # Check if this directory name appears anywhere in the path
                for part in file_path.parts:
                    if fnmatch.fnmatch(part, dir_name):
                        return True
            elif pattern.startswith('**/'):
                # File pattern: **/pattern
                file_pattern = pattern[3:]
                # Check if filename matches
                if fnmatch.fnmatch(file_path.name, file_pattern):
                    return True
        # Handle directory patterns (ending with /)
        elif pattern.endswith('/'):
            dir_pattern = pattern.rstrip('/')
            # Check if this path is within the ignored directory
            for part in file_path.parts:
                if fnmatch.fnmatch(part, dir_pattern):
                    return True
        # Standard patterns
        elif fnmatch.fnmatch(path_str, pattern) or fnmatch.fnmatch(file_path.name, pattern):
            return True
        return False
    
    def analyze_directory(self, directory: Path, use_git: bool = False, no_git: bool = False,
                         max_depth: int = None, verbose: bool = False, debug: bool = False) -> Dict[str, Any]:
        """Analyze directory and return language statistics with encapsulated state."""
        
        results = {
            'languages': defaultdict(lambda: {'files': 0, 'total_lines': 0, 'code_lines': 0, 'comment_lines': 0}),
            'total_files': 0,
            'total_lines': 0,
            'total_code_lines': 0,
            'total_comment_lines': 0,
            'directory': str(directory),
            'unknown_files': [] if debug else None,
            'unknown_extensions': defaultdict(int) if debug else None
        }
        
        # Auto-detect git repository and enable git mode by default
        is_git_repo = self.is_git_repository(directory)
        should_use_git = use_git or (is_git_repo and not no_git)  # Auto-enable git mode in git repos unless disabled
        
        git_patterns = []
        if should_use_git:
            gitignore_path = directory / '.gitignore'
            if gitignore_path.exists():
                git_patterns = self.process_gitignore(gitignore_path)
        
        # Initialize hierarchical ignore context
        pattern_adapter = LineCounterPatternAdapter(self)
        context_factory = IgnoreContextFactory(
            pattern_matcher=pattern_adapter,
            cache_strategy_factory=lambda: LRUCacheStrategy(1000),
            case_insensitive=platform.system() == 'Windows'
        )
        ignore_context = context_factory.create_context(directory)
        if verbose and ignore_context:
            self.logger.info("Processing .ulcignore files hierarchically")
        
        # Store git info in results for display
        results['is_git_repo'] = is_git_repo
        results['using_git'] = should_use_git
        results['using_ulcignore'] = ignore_context is not None
        
        # Track visited directories to prevent infinite recursion with symlinks
        visited_dirs = set()
        
        def analyze_recursively(current_dir: Path, current_depth: int = 0, current_ignore_context=None):
            if max_depth is not None and current_depth > max_depth:
                return
            
            # Resolve directory path to handle symlinks properly
            try:
                resolved_dir = current_dir.resolve()
            except (OSError, RuntimeError) as e:
                self.logger.warning(f"Cannot resolve directory {current_dir}: {e}")
                return  # Skip if can't resolve (broken symlink, etc.)
            
            # Check if we've already visited this directory (prevents infinite recursion)
            if resolved_dir in visited_dirs:
                return
            visited_dirs.add(resolved_dir)
            
            # Update ignore context for hierarchical support
            context = current_ignore_context
            if context_factory:
                if current_dir != directory:  # Not root
                    new_context = context_factory.create_context(current_dir, current_ignore_context)
                    if new_context:
                        context = new_context
                        if verbose:
                            self.logger.debug(f"Found .ulcignore in {current_dir}")
                elif context is None:
                    context = ignore_context
            
            try:
                for item in current_dir.iterdir():
                    # Check if item should be ignored using hierarchical context
                    if context:
                        # Use hierarchical context with debug support
                        if hasattr(context, 'should_ignore_with_context') and debug:
                            is_ignored, ignoring_context = context.should_ignore_with_context(item)
                            if is_ignored and ignoring_context:
                                relative_item = item.relative_to(directory)
                                self.logger.debug(f"Ignored {relative_item} by {ignoring_context.directory}/.ulcignore")
                                continue
                        elif context.should_ignore(item):
                            continue
                    
                    if item.is_dir():
                        if not self.should_ignore_directory(item):
                            analyze_recursively(item, current_depth + 1, context)
                    elif item.is_file():
                        if not self.should_ignore_file(item):
                            relative_path = item.relative_to(directory)
                            if not (use_git and self.is_gitignored(relative_path, git_patterns)):
                                total, code, comment = self.count_lines_in_file(item)
                                if total > 0:
                                    language = self.detect_language(item)
                                    
                                    # Handle unknown files based on debug mode
                                    if language == 'Unknown':
                                        if debug:
                                            # In debug mode, include unknown files
                                            results['unknown_files'].append(str(item.relative_to(directory)))
                                            ext = item.suffix if item.suffix else '<no_extension>'
                                            results['unknown_extensions'][ext] += 1
                                            
                                            # Update language stats for debug mode
                                            results['languages'][language]['files'] += 1
                                            results['languages'][language]['total_lines'] += total
                                            results['languages'][language]['code_lines'] += code
                                            results['languages'][language]['comment_lines'] += comment
                                            
                                            # Update overall stats
                                            results['total_files'] += 1
                                            results['total_lines'] += total
                                            results['total_code_lines'] += code
                                            results['total_comment_lines'] += comment
                                        else:
                                            # In normal mode, skip unknown files (don't count them)
                                            continue
                                    else:
                                        # Known language - always include
                                        results['languages'][language]['files'] += 1
                                        results['languages'][language]['total_lines'] += total
                                        results['languages'][language]['code_lines'] += code
                                        results['languages'][language]['comment_lines'] += comment
                                        
                                        # Update overall stats
                                        results['total_files'] += 1
                                        results['total_lines'] += total
                                        results['total_code_lines'] += code
                                        results['total_comment_lines'] += comment
                                    
                                    if verbose:
                                        print(f"  {item.relative_to(directory)}: {language} ({total} lines)")
            
            except (OSError, PermissionError) as e:
                if verbose:
                    print(f"Warning: Cannot access {current_dir}: {e}")
                self.logger.warning(f"Cannot access directory {current_dir}: {e}")
        
        analyze_recursively(directory, 0, ignore_context)
        return results


# ============================================================================
# COLOR DEFINITIONS
# ============================================================================

class Colors:
    """ANSI color codes for terminal output - thread-safe instance-based design."""
    
    def __init__(self, enabled: bool = True):
        """Initialize colors with enable/disable state."""
        if enabled:
            self.HEADER = '\033[1;36m'      # Bold Cyan
            self.TOTAL = '\033[1;32m'       # Bold Green  
            self.SEPARATOR = '\033[90m'     # Gray
            self.LANGUAGE = '\033[94m'      # Blue
            self.PERCENTAGE = '\033[35m'    # Magenta (neutral, distinctive for all percentages)
            self.DIRECTORY = '\033[96m'     # Cyan
            self.RESET = '\033[0m'          # Reset
        else:
            self.HEADER = ''
            self.TOTAL = ''
            self.SEPARATOR = ''
            self.LANGUAGE = ''
            self.PERCENTAGE = ''
            self.DIRECTORY = ''
            self.RESET = ''


def get_percentage_color(colors: Colors, percentage: float) -> str:
    """Get neutral color for percentage value - all percentages use the same neutral color."""
    return colors.PERCENTAGE  # Use magenta for all percentages


# ============================================================================
# MAIN FUNCTIONALITY
# ============================================================================

def format_results(results: Dict[str, Any], colors: Colors, sort_by: str = 'lines') -> str:
    """Format analysis results for display."""
    output = []
    
    # Header with colon and top separator
    output.append(f"{colors.HEADER}Universal Language Counter Results:{colors.RESET}")
    output.append(f"{colors.SEPARATOR}{'-' * 80}{colors.RESET}")
    output.append(f"{'Language':<20} {'Files':<8} {'Total':<10} {'Code':<10} {'Comments':<10} {'%':<6}")
    output.append(f"{colors.SEPARATOR}{'-' * 80}{colors.RESET}")
    
    # Language breakdown
    languages = results['languages']
    if not languages:
        output.append("No files found or analyzed.")
        return "\n".join(output)
    
    # Sort languages
    if sort_by == 'lines':
        sorted_langs = sorted(languages.items(), key=lambda x: x[1]['total_lines'], reverse=True)
    elif sort_by == 'files':
        sorted_langs = sorted(languages.items(), key=lambda x: x[1]['files'], reverse=True)
    elif sort_by == 'name':
        sorted_langs = sorted(languages.items(), key=lambda x: x[0])
    else:
        sorted_langs = list(languages.items())
    
    # Total row first
    output.append(
        f"{colors.TOTAL}{'Total':<20}{colors.RESET} "
        f"{colors.TOTAL}{results['total_files']:<8}{colors.RESET} "
        f"{colors.TOTAL}{results['total_lines']:<10,}{colors.RESET} "
        f"{colors.TOTAL}{results['total_code_lines']:<10,}{colors.RESET} "
        f"{colors.TOTAL}{results['total_comment_lines']:<10,}{colors.RESET} "
        f"{colors.TOTAL}{'100.0%':<6}{colors.RESET}"
    )
    output.append(f"{colors.SEPARATOR}{'-' * 80}{colors.RESET}")
    
    # Language rows
    for language, stats in sorted_langs:
        percentage = (stats['total_lines'] / results['total_lines'] * 100) if results['total_lines'] > 0 else 0
        percentage_color = get_percentage_color(colors, percentage)
        
        output.append(
            f"{colors.LANGUAGE}{language:<20}{colors.RESET} "
            f"{stats['files']:<8} "
            f"{stats['total_lines']:<10,} "
            f"{stats['code_lines']:<10,} "
            f"{stats['comment_lines']:<10,} "
            f"{percentage_color}{percentage:<5.1f}%{colors.RESET}"
        )
    
    # Bottom separator and directory
    output.append(f"{colors.SEPARATOR}{'-' * 80}{colors.RESET}")
    
    # Show git awareness info
    status_parts = []
    if results.get('is_git_repo'):
        if results.get('using_git'):
            status_parts.append("git repository - respecting .gitignore")
        else:
            status_parts.append("git repository")
    
    if results.get('using_ulcignore'):
        status_parts.append("respecting .ulcignore")
    
    status_text = ""
    if status_parts:
        status_text = f" {colors.LANGUAGE}({', '.join(status_parts)}){colors.RESET}"
    
    output.append(f"Directory: {colors.DIRECTORY}{results['directory']}{colors.RESET}{status_text}")
    
    # Debug information
    if results.get('unknown_files') is not None:
        output.append("")
        output.append(f"{colors.HEADER}Debug Information:{colors.RESET}")
        output.append(f"{colors.SEPARATOR}{'-' * 40}{colors.RESET}")
        
        # Show unknown extensions summary
        if results['unknown_extensions']:
            output.append("Unknown file extensions found:")
            for ext, count in sorted(results['unknown_extensions'].items(), key=lambda x: x[1], reverse=True):
                output.append(f"  {ext}: {count} files")
        
        # Show some example unknown files
        if results['unknown_files']:
            output.append(f"\nExample unknown files (showing first 10):")
            for file_path in results['unknown_files'][:10]:
                output.append(f"  {file_path}")
            
            if len(results['unknown_files']) > 10:
                output.append(f"  ... and {len(results['unknown_files']) - 10} more")
    
    return "\n".join(output)


def main():
    """Main entry point for Universal Language Counter."""
    parser = argparse.ArgumentParser(
        description="Universal Language Counter - Count lines of code across 119+ programming languages",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ulc.py .                          # Count current directory (auto-respects .gitignore in git repos)
  ulc.py /path/to/project           # Auto-detects git and respects .gitignore
  ulc.py . --no-git                 # Ignore .gitignore even in git repos
  ulc.py /non-git/dir --git         # Force .gitignore respect in non-git directory
  ulc.py . --depth 2                # Limit depth to 2 levels
  ulc.py . --sort files             # Sort by file count
  ulc.py . --comprehensive          # Use GitHub Linguist for 400+ languages

Note: .gitignore is automatically respected in git repositories. Use --no-git to disable.
        """
    )
    
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directory to analyze (default: current directory)')
    parser.add_argument('--git', action='store_true',
                       help='Force .gitignore respect in non-git directories (git repos auto-detected)')
    parser.add_argument('--no-git', action='store_true',
                       help='Disable .gitignore (by default, .gitignore is respected in git repos)')
    parser.add_argument('--depth', type=int, metavar='N',
                       help='Maximum directory depth to traverse')
    parser.add_argument('--sort', choices=['lines', 'files', 'name'], default='lines',
                       help='Sort results by lines (default), files, or name')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output showing each file processed')
    parser.add_argument('--comprehensive', action='store_true',
                       help='Use comprehensive mode with GitHub Linguist (400+ languages)')
    parser.add_argument('--linguist-path', metavar='PATH',
                       help='Path to github-linguist executable')
    parser.add_argument('--no-color', action='store_true',
                       help='Disable colored output')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug mode (show unknown files and extension analysis)')
    parser.add_argument('--version', action='version', version='Universal Language Counter 0.1.0')
    
    args = parser.parse_args()
    
    # Create colors instance based on user preference
    colors = Colors(enabled=not args.no_color)
    
    # Configure logging
    if args.debug:
        logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
        # Suppress noisy third-party library debug messages
        logging.getLogger('chardet').setLevel(logging.INFO)
        logging.getLogger('charset_normalizer').setLevel(logging.INFO)
    elif args.verbose:
        logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    else:
        logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')
    
    # Convert directory to Path
    directory = Path(args.directory).resolve()
    
    # Validate directory
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Create LineCounter instance
        counter = LineCounter(
            use_comprehensive=args.comprehensive,
            linguist_cmd=args.linguist_path,
            logger=logging.getLogger(__name__),
            colors=colors
        )
        
        # Analyze directory
        if args.verbose:
            print(f"Analyzing directory: {directory}")
        
        results = counter.analyze_directory(
            directory=directory,
            use_git=args.git,
            no_git=args.no_git,
            max_depth=args.depth,
            verbose=args.verbose,
            debug=args.debug
        )
        
        # Format and display results
        print(format_results(results, colors, args.sort))
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)
    except (ValueError, TypeError) as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"File not found: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"Permission denied: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error in main: {e}", exc_info=True)
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()