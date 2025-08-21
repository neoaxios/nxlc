#!/usr/bin/env python3
"""
Fixture Generator for E2E Line Counting Tests

Generates test fixtures for programming languages with accurate line counts.
Designed for maintainability and easy extension to new languages.
"""

import json
import os
import sys
from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class CommentStyle:
    """Defines comment styles for a programming language."""
    single_line: Optional[str] = None
    multi_line_start: Optional[str] = None
    multi_line_end: Optional[str] = None
    doc_string_delimiters: List[str] = None
    nested_comments: bool = False
    
    def __post_init__(self):
        if self.doc_string_delimiters is None:
            self.doc_string_delimiters = []


@dataclass
class LanguageDefinition:
    """Complete definition of a programming language for testing."""
    name: str
    category: str
    extensions: List[str]
    comment_style: CommentStyle
    keywords: List[str] = None
    string_delimiters: List[str] = None
    escape_char: str = '\\'
    case_sensitive: bool = True
    indent_based: bool = False
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.string_delimiters is None:
            self.string_delimiters = ['"', "'"]


class FixtureTemplate(ABC):
    """Abstract base class for fixture templates."""
    
    @abstractmethod
    def generate(self, language: LanguageDefinition) -> Tuple[str, Dict[str, int]]:
        """
        Generate fixture content and expected counts.
        Returns: (content, counts_dict)
        """
        pass
    
    @abstractmethod
    def get_fixture_type(self) -> str:
        """Get the fixture type name."""
        pass


class SimpleFixtureTemplate(FixtureTemplate):
    """Template for simple fixture files (5-20 lines)."""
    
    def get_fixture_type(self) -> str:
        return "simple"
    
    def generate(self, language: LanguageDefinition) -> Tuple[str, Dict[str, int]]:
        """Generate simple fixture with basic syntax."""
        lines = []
        code_count = 0
        comment_count = 0
        blank_count = 0
        
        # Add header comment
        if language.comment_style.single_line:
            lines.append(f"{language.comment_style.single_line} Simple test file for {language.name}")
            lines.append(f"{language.comment_style.single_line} This tests basic line counting")
            comment_count += 2
        
        # Add blank line
        lines.append("")
        blank_count += 1
        
        # Add simple code based on language
        if language.indent_based:
            # Python-like
            lines.append("def main():")
            lines.append("    x = 42")
            lines.append("    y = x * 2")
            lines.append("    return y")
            code_count += 4
        else:
            # C-like
            lines.append("function main() {")
            lines.append("    var x = 42;")
            lines.append("    var y = x * 2;")
            lines.append("    return y;")
            lines.append("}")
            code_count += 5
        
        # Add blank line
        lines.append("")
        blank_count += 1
        
        # Add inline comment with code
        if language.comment_style.single_line:
            lines.append(f"result = main()  {language.comment_style.single_line} Call the function")
            code_count += 1
            comment_count += 1  # Mixed line counts as both
        else:
            lines.append("result = main()")
            code_count += 1
        
        # Add multi-line comment if supported
        if language.comment_style.multi_line_start:
            lines.append(language.comment_style.multi_line_start)
            lines.append(" * Multi-line comment")
            lines.append(" * Second line")
            lines.append(" " + language.comment_style.multi_line_end)
            comment_count += 4
        
        content = "\n".join(lines)
        total = len(lines)
        
        counts = {
            "total": total,
            "code": code_count,
            "comments": comment_count,
            "blank": blank_count
        }
        
        return content, counts


class ComplexFixtureTemplate(FixtureTemplate):
    """Template for complex fixture files (50-100 lines)."""
    
    def get_fixture_type(self) -> str:
        return "complex"
    
    def generate(self, language: LanguageDefinition) -> Tuple[str, Dict[str, int]]:
        """Generate complex fixture with advanced features."""
        lines = []
        code_count = 0
        comment_count = 0
        blank_count = 0
        
        # File header with multi-line comment
        if language.comment_style.multi_line_start:
            lines.extend([
                language.comment_style.multi_line_start,
                " * Complex test file for " + language.name,
                " * ",
                " * This file tests:",
                " * - Nested comments (if supported)",
                " * - String literals with comment-like content",
                " * - Mixed code and comments",
                " * - Various comment styles",
                " " + language.comment_style.multi_line_end
            ])
            comment_count += 9
        
        lines.append("")
        blank_count += 1
        
        # Import/include statements
        if language.name.lower() == "python":
            lines.extend([
                "import sys",
                "import os",
                "from typing import List, Dict",
                ""
            ])
            code_count += 3
            blank_count += 1
        elif language.name.lower() in ["javascript", "typescript"]:
            lines.extend([
                "import { Component } from 'framework';",
                "import * as utils from './utils';",
                ""
            ])
            code_count += 2
            blank_count += 1
        elif language.name.lower() in ["c", "c++", "java"]:
            lines.extend([
                "#include <stdio.h>",
                "#include <stdlib.h>",
                ""
            ])
            code_count += 2
            blank_count += 1
        
        # Class or function with documentation
        if language.indent_based:
            # Python-style
            lines.extend([
                "class DataProcessor:",
                '    """',
                '    A class for processing data.',
                '    ',
                '    This demonstrates multi-line doc strings.',
                '    """',
                '    ',
                '    def __init__(self, config):',
                '        """Initialize with config."""',
                '        self.config = config',
                f'        self.data = []  {language.comment_style.single_line} Initialize empty data',
                '    ',
                '    def process(self, input_data):',
                '        """',
                '        Process input data.',
                '        ',
                '        Args:',
                '            input_data: The data to process',
                '        """',
                f'        {language.comment_style.single_line} Check if data is valid',
                '        if not input_data:',
                '            return None',
                '        ',
                f'        {language.comment_style.single_line} Process each item',
                '        result = []',
                '        for item in input_data:',
                f'            {language.comment_style.single_line} Skip invalid items',
                '            if self.validate(item):',
                '                processed = self.transform(item)',
                '                result.append(processed)',
                '        ',
                '        return result',
                '    ',
                '    def validate(self, item):',
                '        """Validate an item."""',
                '        return item is not None',
                '    ',
                '    def transform(self, item):',
                '        """Transform an item."""',
                f'        {language.comment_style.single_line} Apply transformation',
                '        return item.upper() if isinstance(item, str) else item'
            ])
            code_count += 25
            comment_count += 15
            blank_count += 5
        else:
            # C-style languages
            lines.extend([
                "class DataProcessor {",
                "    constructor(config) {",
                "        this.config = config;",
                f"        this.data = [];  {language.comment_style.single_line} Initialize empty data",
                "    }",
                "    ",
                "    process(inputData) {",
                f"        {language.comment_style.single_line} Check if data is valid",
                "        if (!inputData) {",
                "            return null;",
                "        }",
                "        ",
                f"        {language.comment_style.single_line} Process each item",
                "        const result = [];",
                "        for (const item of inputData) {",
                f"            {language.comment_style.single_line} Skip invalid items",
                "            if (this.validate(item)) {",
                "                const processed = this.transform(item);",
                "                result.push(processed);",
                "            }",
                "        }",
                "        ",
                "        return result;",
                "    }",
                "    ",
                "    validate(item) {",
                "        return item !== null && item !== undefined;",
                "    }",
                "    ",
                "    transform(item) {",
                f"        {language.comment_style.single_line} Apply transformation",
                "        return typeof item === 'string' ? item.toUpperCase() : item;",
                "    }",
                "}"
            ])
            code_count += 28
            comment_count += 5
            blank_count += 3
        
        # Add string with comment-like content
        lines.append("")
        blank_count += 1
        
        if language.comment_style.single_line:
            comment_char = language.comment_style.single_line
            lines.extend([
                f'message = "This string contains {comment_char} but it\'s not a comment"',
                f'pattern = "{comment_char}.*$"  {comment_char} Regex for matching comments',
                ""
            ])
            code_count += 2
            comment_count += 1
            blank_count += 1
        
        # Add trailing comments
        if language.comment_style.single_line:
            lines.extend([
                language.comment_style.single_line * 50,
                f"{language.comment_style.single_line} End of complex test file",
                language.comment_style.single_line * 50
            ])
            comment_count += 3
        
        content = "\n".join(lines)
        total = len(lines)
        
        counts = {
            "total": total,
            "code": code_count,
            "comments": comment_count,
            "blank": blank_count
        }
        
        return content, counts


class EdgeCasesFixtureTemplate(FixtureTemplate):
    """Template for edge case fixture files (20-50 lines)."""
    
    def get_fixture_type(self) -> str:
        return "edge_cases"
    
    def generate(self, language: LanguageDefinition) -> Tuple[str, Dict[str, int]]:
        """Generate edge cases fixture."""
        lines = []
        code_count = 0
        comment_count = 0
        blank_count = 0
        
        # Unicode comments
        if language.comment_style.single_line:
            lines.extend([
                f"{language.comment_style.single_line} Edge case tests for {language.name}",
                f"{language.comment_style.single_line} Unicode: 你好世界 🌍 مرحبا بالعالم",
                ""
            ])
            comment_count += 2
            blank_count += 1
        
        # String with comment syntax
        lines.extend([
            f'url = "http://example.com{language.comment_style.single_line}not-a-comment"',
            f'regex = r"{language.comment_style.single_line}\\s*(.*)$"  {language.comment_style.single_line} Pattern to match comments',
            ""
        ])
        code_count += 2
        comment_count += 1
        blank_count += 1
        
        # Escaped characters in strings
        if language.escape_char:
            lines.extend([
                f'escaped = "This has \\"quotes\\" and \\{language.escape_char}n newlines"',
                f'path = "C:{language.escape_char}{language.escape_char}Users{language.escape_char}{language.escape_char}file.txt"',
                ""
            ])
            code_count += 2
            blank_count += 1
        
        # Nested comments if supported
        if language.comment_style.nested_comments and language.comment_style.multi_line_start:
            lines.extend([
                language.comment_style.multi_line_start,
                " Outer comment",
                " " + language.comment_style.multi_line_start,
                " Nested comment",
                " " + language.comment_style.multi_line_end,
                " Still in outer comment",
                language.comment_style.multi_line_end,
                ""
            ])
            comment_count += 7
            blank_count += 1
        
        # Mixed line endings (simulated)
        lines.append(f"mixed_endings = 'line1\\rline2\\nline3\\r\\n'  {language.comment_style.single_line} Different line endings")
        code_count += 1
        comment_count += 1
        
        # Very long line
        long_line = "x = " + " + ".join([str(i) for i in range(50)])
        if language.comment_style.single_line:
            long_line += f"  {language.comment_style.single_line} Long line with many operations"
            comment_count += 1
        lines.append(long_line)
        code_count += 1
        
        # Empty comment
        if language.comment_style.single_line:
            lines.extend([
                "",
                language.comment_style.single_line,
                language.comment_style.single_line + " ",
                ""
            ])
            comment_count += 2
            blank_count += 2
        
        # Multiple blank lines
        lines.extend(["", "", ""])
        blank_count += 3
        
        # Code that looks like comments
        lines.append(f'comment_marker = "{language.comment_style.single_line}"')
        code_count += 1
        
        if language.comment_style.multi_line_start:
            lines.append(f'block_start = "{language.comment_style.multi_line_start}"')
            lines.append(f'block_end = "{language.comment_style.multi_line_end}"')
            code_count += 2
        
        # Trailing whitespace with comment
        if language.comment_style.single_line:
            lines.append(f"trailing = 'value'    {language.comment_style.single_line} Comment after spaces    ")
            code_count += 1
            comment_count += 1
        
        content = "\n".join(lines)
        total = len(lines)
        
        counts = {
            "total": total,
            "code": code_count,
            "comments": comment_count,
            "blank": blank_count
        }
        
        return content, counts


class LanguageRegistry:
    """Registry of language definitions."""
    
    _languages: Dict[str, LanguageDefinition] = {}
    
    @classmethod
    def register(cls, language: LanguageDefinition):
        """Register a language definition."""
        cls._languages[language.name.lower()] = language
    
    @classmethod
    def get(cls, name: str) -> Optional[LanguageDefinition]:
        """Get a language definition by name."""
        return cls._languages.get(name.lower())
    
    @classmethod
    def list_languages(cls) -> List[str]:
        """List all registered languages."""
        return sorted(cls._languages.keys())
    
    @classmethod
    def list_by_category(cls) -> Dict[str, List[str]]:
        """List languages grouped by category."""
        by_category = {}
        for lang in cls._languages.values():
            if lang.category not in by_category:
                by_category[lang.category] = []
            by_category[lang.category].append(lang.name)
        return by_category
    
    @classmethod
    def initialize_defaults(cls):
        """Initialize with default language definitions."""
        # Python
        cls.register(LanguageDefinition(
            name="Python",
            category="common",
            extensions=[".py", ".pyw"],
            comment_style=CommentStyle(
                single_line="#",
                doc_string_delimiters=['"""', "'''"]
            ),
            keywords=["def", "class", "import", "from", "if", "else", "elif",
                     "for", "while", "return", "yield", "lambda", "async", "await"],
            indent_based=True
        ))
        
        # JavaScript
        cls.register(LanguageDefinition(
            name="JavaScript",
            category="common",
            extensions=[".js", ".mjs", ".cjs"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["function", "var", "let", "const", "if", "else", "for",
                     "while", "return", "class", "async", "await", "import", "export"]
        ))
        
        # Java
        cls.register(LanguageDefinition(
            name="Java",
            category="common",
            extensions=[".java"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/",
                doc_string_delimiters=["/**", "*/"]
            ),
            keywords=["public", "private", "protected", "class", "interface",
                     "extends", "implements", "static", "final", "void", "return"]
        ))
        
        # C++
        cls.register(LanguageDefinition(
            name="C++",
            category="common",
            extensions=[".cpp", ".cc", ".cxx", ".hpp", ".hxx", ".h"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["class", "struct", "namespace", "template", "typename",
                     "public", "private", "protected", "virtual", "override"]
        ))
        
        # C
        cls.register(LanguageDefinition(
            name="C",
            category="common",
            extensions=[".c", ".h"],
            comment_style=CommentStyle(
                single_line="//",  # C99+
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["struct", "typedef", "enum", "union", "void", "return",
                     "if", "else", "for", "while", "switch", "case"]
        ))
        
        # TypeScript
        cls.register(LanguageDefinition(
            name="TypeScript",
            category="web",
            extensions=[".ts", ".tsx"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["interface", "type", "enum", "namespace", "declare",
                     "abstract", "implements", "extends", "async", "await"]
        ))
        
        # Go
        cls.register(LanguageDefinition(
            name="Go",
            category="systems",
            extensions=[".go"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["package", "import", "func", "var", "const", "type",
                     "struct", "interface", "defer", "go", "chan", "select"]
        ))
        
        # Rust
        cls.register(LanguageDefinition(
            name="Rust",
            category="systems",
            extensions=[".rs"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/",
                nested_comments=True
            ),
            keywords=["fn", "let", "mut", "const", "struct", "enum", "trait",
                     "impl", "mod", "use", "pub", "async", "await", "match"]
        ))
        
        # Ruby
        cls.register(LanguageDefinition(
            name="Ruby",
            category="scripting",
            extensions=[".rb"],
            comment_style=CommentStyle(
                single_line="#",
                multi_line_start="=begin",
                multi_line_end="=end"
            ),
            keywords=["def", "class", "module", "if", "unless", "else", "elsif",
                     "case", "when", "while", "until", "for", "do", "end"]
        ))
        
        # PHP
        cls.register(LanguageDefinition(
            name="PHP",
            category="web",
            extensions=[".php"],
            comment_style=CommentStyle(
                single_line="//",
                multi_line_start="/*",
                multi_line_end="*/"
            ),
            keywords=["<?php", "?>", "function", "class", "namespace", "use",
                     "public", "private", "protected", "static", "return"]
        ))


class FixtureGenerator:
    """Main fixture generator class."""
    
    def __init__(self, base_dir: Path):
        """Initialize with base directory for fixtures."""
        self.base_dir = base_dir
        self.templates = [
            SimpleFixtureTemplate(),
            ComplexFixtureTemplate(),
            EdgeCasesFixtureTemplate()
        ]
    
    def generate_language_fixtures(self, 
                                  language: LanguageDefinition,
                                  force: bool = False) -> bool:
        """Generate all fixtures for a language."""
        # Create language directory
        lang_dir = self.base_dir / language.category / language.name.lower()
        lang_dir.mkdir(parents=True, exist_ok=True)
        
        # Check if fixtures already exist
        expected_file = lang_dir / "expected.json"
        if expected_file.exists() and not force:
            logger.info(f"Fixtures already exist for {language.name}. Use --force to overwrite.")
            return False
        
        # Generate fixtures
        expected_data = {
            "language": language.name,
            "category": language.category,
            "extensions": language.extensions
        }
        
        for template in self.templates:
            fixture_type = template.get_fixture_type()
            logger.info(f"Generating {fixture_type} fixture for {language.name}")
            
            content, counts = template.generate(language)
            
            # Determine file extension
            ext = language.extensions[0] if language.extensions else ".txt"
            filename = f"{fixture_type}{ext}"
            
            # Write fixture file
            fixture_path = lang_dir / filename
            with open(fixture_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Add to expected data
            expected_data[fixture_type] = {
                "filename": filename,
                **counts
            }
        
        # Write expected.json
        with open(expected_file, 'w') as f:
            json.dump(expected_data, f, indent=2)
        
        logger.info(f"Generated fixtures for {language.name} in {lang_dir}")
        return True
    
    def generate_category(self, category: str) -> int:
        """Generate fixtures for all languages in a category."""
        count = 0
        languages = LanguageRegistry.list_by_category().get(category, [])
        
        for lang_name in languages:
            language = LanguageRegistry.get(lang_name)
            if language and self.generate_language_fixtures(language):
                count += 1
        
        return count
    
    def generate_all(self) -> int:
        """Generate fixtures for all registered languages."""
        count = 0
        for lang_name in LanguageRegistry.list_languages():
            language = LanguageRegistry.get(lang_name)
            if language and self.generate_language_fixtures(language):
                count += 1
        
        return count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Generate E2E test fixtures')
    parser.add_argument('--language', '-l', help='Generate fixtures for specific language')
    parser.add_argument('--category', '-c', help='Generate fixtures for category')
    parser.add_argument('--all', action='store_true', help='Generate all fixtures')
    parser.add_argument('--list', action='store_true', help='List available languages')
    parser.add_argument('--force', '-f', action='store_true', help='Overwrite existing fixtures')
    parser.add_argument('--output', '-o', type=Path, 
                       default=Path(__file__).parent / 'fixtures',
                       help='Output directory for fixtures')
    
    args = parser.parse_args()
    
    # Initialize language registry
    LanguageRegistry.initialize_defaults()
    
    if args.list:
        print("Available languages by category:")
        for category, languages in LanguageRegistry.list_by_category().items():
            print(f"\n{category}:")
            for lang in sorted(languages):
                print(f"  - {lang}")
        return 0
    
    generator = FixtureGenerator(args.output)
    
    if args.language:
        language = LanguageRegistry.get(args.language)
        if not language:
            logger.error(f"Language '{args.language}' not found")
            return 1
        
        if generator.generate_language_fixtures(language, args.force):
            print(f"Generated fixtures for {language.name}")
        return 0
    
    elif args.category:
        count = generator.generate_category(args.category)
        print(f"Generated fixtures for {count} languages in category '{args.category}'")
        return 0
    
    elif args.all:
        count = generator.generate_all()
        print(f"Generated fixtures for {count} languages")
        return 0
    
    else:
        parser.print_help()
        return 1


if __name__ == '__main__':
    sys.exit(main())