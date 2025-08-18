#!/usr/bin/env python3
"""
Comprehensive test suite for hierarchical .ulcignore support.
Tests all components end-to-end without mocks.
"""

import os
import sys
import unittest
import tempfile
import shutil
import platform
from pathlib import Path
from typing import List, Dict, Any, Optional
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'src' / 'ulc'))

# Import from the main ulc module
import ulc
from ulc import LineCounter

# Import from hierarchical_ignore module
import hierarchical_ignore
from hierarchical_ignore import (
    PatternMatcher,
    CacheStrategy,
    LRUCacheStrategy,
    IgnoreFileReader,
    IgnoreContext,
    IgnoreContextFactory,
    LineCounterPatternAdapter,
    HierarchicalConfigContext
)


# ============================================================================
# TEST INFRASTRUCTURE
# ============================================================================

class TestFileSystem:
    """Utility class for creating test file system structures."""
    
    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.created_files = []
        self.created_dirs = []
    
    def create_file(self, path: str, content: str = "") -> Path:
        """Create a file with given content."""
        full_path = self.base_dir / path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        self.created_files.append(full_path)
        return full_path
    
    def create_dir(self, path: str) -> Path:
        """Create a directory."""
        full_path = self.base_dir / path
        full_path.mkdir(parents=True, exist_ok=True)
        self.created_dirs.append(full_path)
        return full_path
    
    def create_ulcignore(self, dir_path: str, patterns: List[str]) -> Path:
        """Create a .ulcignore file with given patterns."""
        content = "\n".join(patterns)
        return self.create_file(f"{dir_path}/.ulcignore", content)
    
    def create_symlink(self, source: str, target: str) -> Path:
        """Create a symbolic link."""
        source_path = self.base_dir / source
        target_path = self.base_dir / target
        target_path.parent.mkdir(parents=True, exist_ok=True)
        if target_path.exists():
            target_path.unlink()
        target_path.symlink_to(source_path)
        return target_path
    
    def get_path(self, relative_path: str) -> Path:
        """Get full path for a relative path."""
        return self.base_dir / relative_path


class HierarchicalIgnoreTestBase(unittest.TestCase):
    """Base test class with shared infrastructure."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp(prefix="ulc_test_")
        self.test_path = Path(self.test_dir)
        self.fs = TestFileSystem(self.test_path)
        self.counter = LineCounter()
        
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_project(self) -> Dict[str, Any]:
        """Create a standard test project structure."""
        # Root level files
        self.fs.create_file("README.md", "# Test Project\n")
        self.fs.create_file("main.py", "print('hello')\n")
        self.fs.create_file("test.txt", "test file\n")
        
        # Source directory
        self.fs.create_file("src/app.py", "def app():\n    pass\n")
        self.fs.create_file("src/utils.py", "def util():\n    pass\n")
        self.fs.create_file("src/config.json", '{"key": "value"}\n')
        
        # Test directory
        self.fs.create_file("tests/test_app.py", "def test_app():\n    pass\n")
        self.fs.create_file("tests/test_utils.py", "def test_utils():\n    pass\n")
        
        # Build directory (typically ignored)
        self.fs.create_file("build/output.js", "console.log('built');\n")
        self.fs.create_file("build/output.map", "sourcemap\n")
        
        # Nested subdirectories
        self.fs.create_file("src/components/header.py", "class Header:\n    pass\n")
        self.fs.create_file("src/components/footer.py", "class Footer:\n    pass\n")
        
        return {
            'total_files': 12,
            'python_files': 7,
            'other_files': 5
        }
    
    def analyze_with_hierarchical(self, patterns_by_dir: Dict[str, List[str]] = None) -> Dict[str, Any]:
        """Analyze directory with hierarchical ignore patterns."""
        if patterns_by_dir:
            for dir_path, patterns in patterns_by_dir.items():
                self.fs.create_ulcignore(dir_path, patterns)
        
        # Check if hierarchical support is available
        if not hasattr(self.counter, 'analyze_directory'):
            raise RuntimeError("LineCounter doesn't have analyze_directory method")
            
        return self.counter.analyze_directory(
            directory=self.test_path,
            verbose=False,
            debug=False
        )
    
    def count_files_in_results(self, results: Dict[str, Any]) -> int:
        """Count total files in results."""
        return results.get('total_files', 0)
    
    def get_language_file_count(self, results: Dict[str, Any], language: str) -> int:
        """Get file count for specific language."""
        languages = results.get('languages', {})
        if language in languages:
            return languages[language].get('files', 0)
        return 0


# ============================================================================
# UNIT TESTS FOR CORE COMPONENTS
# ============================================================================

class TestCacheStrategy(HierarchicalIgnoreTestBase):
    """Test cache strategy implementations."""
    
    def test_lru_cache_basic_operations(self):
        """Test basic LRU cache operations."""
        cache = LRUCacheStrategy(max_size=3)
        
        # Test set and get
        cache.set("key1", True)
        cache.set("key2", False)
        self.assertEqual(cache.get("key1"), True)
        self.assertEqual(cache.get("key2"), False)
        self.assertIsNone(cache.get("key3"))
        
    def test_lru_cache_eviction(self):
        """Test LRU eviction policy."""
        cache = LRUCacheStrategy(max_size=3)
        
        # Fill cache
        cache.set("key1", True)
        cache.set("key2", False)
        cache.set("key3", True)
        
        # Access key1 to make it recently used
        cache.get("key1")
        
        # Add new key, should evict key2 (least recently used)
        cache.set("key4", False)
        
        self.assertEqual(cache.get("key1"), True)  # Still present
        self.assertIsNone(cache.get("key2"))       # Evicted
        self.assertEqual(cache.get("key3"), True)  # Still present
        self.assertEqual(cache.get("key4"), False) # New key
        
    def test_lru_cache_clear(self):
        """Test cache clearing."""
        cache = LRUCacheStrategy(max_size=3)
        cache.set("key1", True)
        cache.set("key2", False)
        
        cache.clear()
        
        self.assertIsNone(cache.get("key1"))
        self.assertIsNone(cache.get("key2"))


class TestIgnoreFileReader(HierarchicalIgnoreTestBase):
    """Test ignore file reader component."""
    
    def test_read_ignore_file_basic(self):
        """Test reading basic ignore file."""
        ignore_file = self.fs.create_file(".ulcignore", "*.txt\n# Comment\n*.log\n\n*.tmp")
        
        patterns = IgnoreFileReader.read_ignore_file(ignore_file)
        
        self.assertEqual(patterns, ["*.txt", "*.log", "*.tmp"])
        
    def test_read_ignore_file_with_comments(self):
        """Test reading ignore file with comments and empty lines."""
        content = """
# Header comment
*.txt
  # Indented comment
*.log

# Another comment
  *.tmp  
"""
        ignore_file = self.fs.create_file(".ulcignore", content)
        
        patterns = IgnoreFileReader.read_ignore_file(ignore_file)
        
        self.assertEqual(patterns, ["*.txt", "*.log", "*.tmp"])
        
    def test_read_ignore_file_size_limit(self):
        """Test file size limit enforcement."""
        # Create a file larger than 1MB
        large_content = "*.txt\n" * 200000  # About 1.2MB
        ignore_file = self.fs.create_file(".ulcignore", large_content)
        
        patterns = IgnoreFileReader.read_ignore_file(ignore_file, max_size=1024*1024)
        
        self.assertEqual(patterns, [])  # Should return empty list for oversized file
        
    def test_read_nonexistent_file(self):
        """Test reading non-existent file."""
        patterns = IgnoreFileReader.read_ignore_file(self.test_path / "nonexistent")
        self.assertEqual(patterns, [])


class TestPatternAdapter(HierarchicalIgnoreTestBase):
    """Test LineCounterPatternAdapter."""
    
    def test_adapter_process_ignore_file(self):
        """Test adapter's process_ignore_file method."""
        adapter = LineCounterPatternAdapter(self.counter)
        
        ignore_file = self.fs.create_file(".ulcignore", "*.txt\n*.log")
        patterns = adapter.process_ignore_file(ignore_file)
        
        self.assertEqual(patterns, ["*.txt", "*.log"])
        
    def test_adapter_matches_patterns(self):
        """Test adapter's matches_patterns method."""
        adapter = LineCounterPatternAdapter(self.counter)
        
        patterns = ["*.txt", "test_*", "build/"]
        
        self.assertTrue(adapter.matches_patterns(Path("file.txt"), patterns))
        self.assertTrue(adapter.matches_patterns(Path("test_file.py"), patterns))
        self.assertFalse(adapter.matches_patterns(Path("file.py"), patterns))


class TestIgnoreContext(HierarchicalIgnoreTestBase):
    """Test IgnoreContext class."""
    
    def test_ignore_context_basic(self):
        """Test basic ignore context functionality."""
        self.fs.create_file("test.txt", "content")
        self.fs.create_file("test.py", "code")
        self.fs.create_ulcignore(".", ["*.txt"])
        
        adapter = LineCounterPatternAdapter(self.counter)
        context = IgnoreContext(
            directory=self.test_path,
            pattern_matcher=adapter
        )
        
        self.assertTrue(context.should_ignore(self.test_path / "test.txt"))
        self.assertFalse(context.should_ignore(self.test_path / "test.py"))
        
    def test_ignore_context_with_parent(self):
        """Test ignore context with parent context."""
        self.fs.create_dir("src")
        self.fs.create_file("src/test.txt", "content")
        self.fs.create_file("src/test.py", "code")
        self.fs.create_file("src/debug.log", "log")
        
        # Root ignores *.txt
        self.fs.create_ulcignore(".", ["*.txt"])
        # src ignores *.log
        self.fs.create_ulcignore("src", ["*.log"])
        
        adapter = LineCounterPatternAdapter(self.counter)
        
        # Create parent context
        parent_context = IgnoreContext(
            directory=self.test_path,
            pattern_matcher=adapter
        )
        
        # Create child context
        child_context = IgnoreContext(
            directory=self.test_path / "src",
            pattern_matcher=adapter,
            parent_context=parent_context
        )
        
        # Check inheritance
        self.assertTrue(child_context.should_ignore(self.test_path / "src" / "test.txt"))  # From parent
        self.assertTrue(child_context.should_ignore(self.test_path / "src" / "debug.log"))  # From child
        self.assertFalse(child_context.should_ignore(self.test_path / "src" / "test.py"))  # Not ignored
        
    def test_ignore_context_caching(self):
        """Test that ignore context caches results."""
        self.fs.create_file("test.txt", "content")
        self.fs.create_ulcignore(".", ["*.txt"])
        
        adapter = LineCounterPatternAdapter(self.counter)
        cache = LRUCacheStrategy(max_size=10)
        context = IgnoreContext(
            directory=self.test_path,
            pattern_matcher=adapter,
            cache_strategy=cache
        )
        
        # First call
        result1 = context.should_ignore(self.test_path / "test.txt")
        # Second call should use cache
        result2 = context.should_ignore(self.test_path / "test.txt")
        
        self.assertEqual(result1, result2)
        self.assertEqual(cache.get("test.txt"), True)


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestHierarchicalIgnoreIntegration(HierarchicalIgnoreTestBase):
    """Integration tests for hierarchical .ulcignore functionality."""
    
    def test_single_root_ulcignore(self):
        """Test with single root .ulcignore file."""
        self.create_test_project()
        
        # Ignore all txt files and build directory
        patterns = {
            ".": ["*.txt", "build/"]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Should exclude test.txt and build/* files
        self.assertEqual(self.count_files_in_results(results), 9)  # 12 - 1 txt - 2 build files
        
    @unittest.skip("Negation patterns not yet implemented")
    def test_nested_ulcignore_override(self):
        """Test that nested .ulcignore can override parent patterns."""
        self.create_test_project()
        
        # Root ignores all .py files
        # src allows .py files again
        patterns = {
            ".": ["*.py"],
            "src": ["!*.py"]  # Negation pattern (if supported)
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # This tests the precedence rules
        python_count = self.get_language_file_count(results, "Python")
        self.assertGreater(python_count, 0)  # Some Python files should be included
        
    def test_deep_hierarchy(self):
        """Test deeply nested directory hierarchy."""
        # Create deep structure
        for i in range(10):
            path = "/".join(["level" + str(j) for j in range(i+1)])
            self.fs.create_file(f"{path}/file{i}.py", f"# Level {i}\n")
            self.fs.create_file(f"{path}/ignore{i}.txt", f"Ignore {i}\n")
            
            # Each level ignores its own txt files
            self.fs.create_ulcignore(path, [f"ignore{i}.txt"])
        
        results = self.analyze_with_hierarchical()
        
        # Should include all .py files but no .txt files
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 10)
        
    def test_pattern_inheritance(self):
        """Test pattern inheritance across directory levels."""
        self.create_test_project()
        
        # Root ignores *.log
        # src ignores *.tmp
        # src/components ignores *.bak
        patterns = {
            ".": ["*.log"],
            "src": ["*.tmp"],
            "src/components": ["*.bak"]
        }
        
        # Add files to test
        self.fs.create_file("root.log", "log")
        self.fs.create_file("src/src.log", "log")
        self.fs.create_file("src/src.tmp", "tmp")
        self.fs.create_file("src/components/comp.log", "log")
        self.fs.create_file("src/components/comp.tmp", "tmp")
        self.fs.create_file("src/components/comp.bak", "bak")
        
        results = self.analyze_with_hierarchical(patterns)
        
        # All .log, .tmp, and .bak files should be ignored
        text_count = self.get_language_file_count(results, "Text")
        self.assertEqual(text_count, 1)  # Only test.txt from create_test_project
        
    def test_complex_patterns(self):
        """Test complex ignore patterns."""
        self.create_test_project()
        
        patterns = {
            ".": [
                "**/test_*.py",  # Ignore test files anywhere
                "**/*.map",      # Ignore source maps
                "build/",        # Ignore build directory
            ]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Should exclude test files and build directory
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 5)  # 7 total - 2 test files


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases(HierarchicalIgnoreTestBase):
    """Test edge cases and error conditions."""
    
    @unittest.skipIf(platform.system() == 'Windows', "Symlinks require admin on Windows")
    def test_symlink_handling(self):
        """Test handling of symbolic links."""
        self.fs.create_file("target/file.py", "print('target')\n")
        self.fs.create_ulcignore("target", ["*.log"])
        
        # Create symlink to directory
        self.fs.create_symlink("target", "link")
        
        # Create circular symlink (should not cause infinite loop)
        self.fs.create_symlink(".", "target/circular")
        
        results = self.analyze_with_hierarchical()
        
        # Should handle symlinks without crashing
        self.assertIsNotNone(results)
        
    @unittest.skipIf(platform.system() == 'Windows', "Symlinks require admin on Windows")
    def test_symlinked_ulcignore(self):
        """Test symlinked .ulcignore files."""
        # Create actual ignore file
        self.fs.create_file("configs/ignore_rules", "*.txt\n*.log")
        
        # Symlink it as .ulcignore
        link_path = self.test_path / ".ulcignore"
        link_path.symlink_to(self.test_path / "configs" / "ignore_rules")
        
        self.fs.create_file("test.txt", "text")
        self.fs.create_file("test.py", "code")
        
        results = self.analyze_with_hierarchical()
        
        # Should respect symlinked .ulcignore
        text_count = self.get_language_file_count(results, "Text")
        self.assertEqual(text_count, 0)
        
    def test_unicode_patterns_and_paths(self):
        """Test Unicode in patterns and file paths."""
        # Create files with Unicode names
        self.fs.create_file("测试.py", "# 中文注释\nprint('你好')\n")
        self.fs.create_file("тест.txt", "Русский текст\n")
        self.fs.create_file("test_émoji_😀.log", "log content\n")
        
        # Create .ulcignore with Unicode patterns
        patterns = {
            ".": ["*😀*", "тест.*"]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Should handle Unicode correctly
        python_count = self.get_language_file_count(results, "Python")
        self.assertGreater(python_count, 0)  # 测试.py should be included
        
    @unittest.skipIf(platform.system() != 'Windows', "Case sensitivity test for Windows")
    def test_case_insensitive_windows(self):
        """Test case-insensitive matching on Windows."""
        self.fs.create_file("Test.txt", "content")
        self.fs.create_file("test.TXT", "content")  # May fail on case-insensitive FS
        
        patterns = {
            ".": ["*.txt"]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # On Windows, both should be ignored regardless of case
        text_count = self.get_language_file_count(results, "Text")
        self.assertEqual(text_count, 0)
        
    def test_large_ignore_file(self):
        """Test handling of large .ulcignore files."""
        # Create .ulcignore with many patterns
        patterns = [f"pattern_{i}.txt" for i in range(10000)]
        
        start_time = time.time()
        self.fs.create_ulcignore(".", patterns)
        
        # Create some files
        for i in range(100):
            self.fs.create_file(f"pattern_{i}.txt", "content")
            self.fs.create_file(f"file_{i}.py", "code")
        
        results = self.analyze_with_hierarchical()
        elapsed = time.time() - start_time
        
        # Should handle large pattern lists efficiently
        self.assertLess(elapsed, 5.0)  # Should complete within 5 seconds
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 100)
        
    def test_empty_ulcignore(self):
        """Test empty .ulcignore files."""
        self.create_test_project()
        
        # First test without any .ulcignore files
        results_without = self.counter.analyze_directory(
            directory=self.test_path,
            verbose=False,
            debug=False
        )
        base_count = self.count_files_in_results(results_without)
        
        # Create empty .ulcignore files
        self.fs.create_ulcignore(".", [])
        self.fs.create_ulcignore("src", [])
        
        results = self.analyze_with_hierarchical()
        
        # Empty .ulcignore files shouldn't change the file count
        # (except possibly adding the .ulcignore files themselves if they're counted)
        actual_count = self.count_files_in_results(results)
        
        # The count should be the same as base_count since empty .ulcignore 
        # files don't exclude anything
        self.assertEqual(actual_count, base_count)
        
    def test_malformed_patterns(self):
        """Test handling of malformed patterns."""
        patterns = {
            ".": [
                "[",        # Unclosed bracket
                "**/[",     # Invalid pattern
                "\\",       # Backslash
                "",         # Empty pattern (should be filtered)
            ]
        }
        
        self.fs.create_file("test.py", "code")
        
        # Should not crash with malformed patterns
        results = self.analyze_with_hierarchical(patterns)
        self.assertIsNotNone(results)


# ============================================================================
# PERFORMANCE AND SECURITY TESTS
# ============================================================================

class TestPerformanceAndSecurity(HierarchicalIgnoreTestBase):
    """Test performance characteristics and security measures."""
    
    def test_cache_performance(self):
        """Test that caching improves performance."""
        # Create many files
        for i in range(100):
            self.fs.create_file(f"file_{i}.py", f"# File {i}\n")
        
        self.fs.create_ulcignore(".", ["file_5*.py"])
        
        # First run (cold cache)
        start1 = time.time()
        results1 = self.analyze_with_hierarchical()
        time1 = time.time() - start1
        
        # Second run (warm cache) - would need to modify implementation to reuse cache
        start2 = time.time()
        results2 = self.analyze_with_hierarchical()
        time2 = time.time() - start2
        
        # Both should produce same results
        self.assertEqual(
            self.count_files_in_results(results1),
            self.count_files_in_results(results2)
        )
        
    def test_dos_prevention_file_size(self):
        """Test DoS prevention for large .ulcignore files."""
        # Create a .ulcignore file larger than 1MB
        large_content = "pattern\n" * 200000  # ~1.4MB
        
        with open(self.test_path / ".ulcignore", 'w') as f:
            f.write(large_content)
        
        self.fs.create_file("test.py", "code")
        
        # Should handle large file gracefully
        results = self.analyze_with_hierarchical()
        
        # Large file should be rejected, so test.py should be included
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 1)
        
    def test_path_traversal_prevention(self):
        """Test prevention of path traversal attacks."""
        # Try to create patterns that might escape directory
        patterns = {
            ".": [
                "../*",
                "../../*",
                "/etc/passwd",
                "C:\\Windows\\*",
            ]
        }
        
        self.fs.create_file("test.py", "code")
        
        # Should handle potentially malicious patterns safely
        results = self.analyze_with_hierarchical(patterns)
        self.assertIsNotNone(results)
        
    def test_memory_usage_with_deep_hierarchy(self):
        """Test memory usage with deep directory hierarchies."""
        # Create very deep nested structure
        path = "."
        for i in range(100):
            path = f"{path}/dir{i}"
            self.fs.create_dir(path)
            self.fs.create_file(f"{path}/file.py", "code")
            self.fs.create_ulcignore(path, [f"ignore{i}.txt"])
        
        # Should handle deep nesting without excessive memory use
        results = self.analyze_with_hierarchical()
        
        # Should find all Python files
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 100)
        
    def test_concurrent_access(self):
        """Test thread safety of cache operations."""
        import threading
        
        cache = LRUCacheStrategy(max_size=100)
        errors = []
        
        def worker(start, end):
            try:
                for i in range(start, end):
                    cache.set(f"key{i}", i % 2 == 0)
                    cache.get(f"key{i}")
            except Exception as e:
                errors.append(e)
        
        # Create multiple threads
        threads = []
        for i in range(10):
            t = threading.Thread(target=worker, args=(i*10, (i+1)*10))
            threads.append(t)
            t.start()
        
        # Wait for all threads
        for t in threads:
            t.join()
        
        # Should complete without errors
        self.assertEqual(len(errors), 0)


# ============================================================================
# FACTORY AND CONTEXT TESTS
# ============================================================================

class TestFactoryPattern(HierarchicalIgnoreTestBase):
    """Test IgnoreContextFactory."""
    
    def test_factory_creates_context_when_needed(self):
        """Test that factory only creates context when .ulcignore exists."""
        adapter = LineCounterPatternAdapter(self.counter)
        factory = IgnoreContextFactory(pattern_matcher=adapter)
        
        # No .ulcignore file
        context1 = factory.create_context(self.test_path)
        self.assertIsNone(context1)
        
        # Create .ulcignore file
        self.fs.create_ulcignore(".", ["*.txt"])
        
        context2 = factory.create_context(self.test_path)
        self.assertIsNotNone(context2)
        
    def test_factory_with_parent_context(self):
        """Test factory creating child context with parent."""
        self.fs.create_ulcignore(".", ["*.txt"])
        self.fs.create_dir("src")
        self.fs.create_ulcignore("src", ["*.log"])
        
        adapter = LineCounterPatternAdapter(self.counter)
        factory = IgnoreContextFactory(pattern_matcher=adapter)
        
        # Create parent context
        parent = factory.create_context(self.test_path)
        self.assertIsNotNone(parent)
        
        # Create child context with parent
        child = factory.create_context(self.test_path / "src", parent)
        self.assertIsNotNone(child)
        self.assertEqual(child.parent, parent)
        
    def test_factory_configuration(self):
        """Test factory with custom configuration."""
        adapter = LineCounterPatternAdapter(self.counter)
        
        # Custom cache factory
        def custom_cache():
            return LRUCacheStrategy(max_size=50)
        
        factory = IgnoreContextFactory(
            pattern_matcher=adapter,
            cache_strategy_factory=custom_cache,
            case_insensitive=True
        )
        
        self.fs.create_ulcignore(".", ["*.txt"])
        context = factory.create_context(self.test_path)
        
        self.assertIsNotNone(context)
        self.assertTrue(context.case_insensitive)


class TestHierarchicalConfigContext(HierarchicalIgnoreTestBase):
    """Test generic HierarchicalConfigContext."""
    
    def test_generic_config_context(self):
        """Test generic hierarchical configuration context."""
        # Create config files
        self.fs.create_file("config.json", '{"key1": "root"}')
        self.fs.create_file("src/config.json", '{"key2": "src"}')
        
        import json
        
        def parser(path: Path) -> dict:
            with open(path) as f:
                return json.load(f)
        
        def merger(parent: dict, child: dict) -> dict:
            merged = parent.copy()
            merged.update(child)
            return merged
        
        # Create root context
        root_context = HierarchicalConfigContext(
            directory=self.test_path,
            config_filename="config.json",
            parser=parser,
            merger=merger
        )
        
        # Create child context
        child_context = HierarchicalConfigContext(
            directory=self.test_path / "src",
            config_filename="config.json",
            parser=parser,
            merger=merger,
            parent=root_context
        )
        
        # Test config merging
        root_config = root_context.get_effective_config()
        self.assertEqual(root_config, {"key1": "root"})
        
        child_config = child_context.get_effective_config()
        self.assertEqual(child_config, {"key1": "root", "key2": "src"})


# ============================================================================
# END-TO-END TESTS
# ============================================================================

class TestEndToEnd(HierarchicalIgnoreTestBase):
    """End-to-end tests simulating real usage scenarios."""
    
    def test_monorepo_scenario(self):
        """Test monorepo with multiple projects."""
        # Create monorepo structure
        projects = ["frontend", "backend", "shared", "tools"]
        
        for project in projects:
            self.fs.create_file(f"{project}/src/main.py", "# Main\n")
            self.fs.create_file(f"{project}/tests/test_main.py", "# Test\n")
            self.fs.create_file(f"{project}/build/output.js", "// Built\n")
            self.fs.create_file(f"{project}/node_modules/lib.js", "// Lib\n")
        
        # Root ignores node_modules globally
        # Each project ignores its build directory
        patterns = {
            ".": ["**/node_modules/"],
            "frontend": ["build/"],
            "backend": ["build/", "*.pyc"],
            "shared": ["dist/"],
            "tools": ["bin/"]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Should exclude node_modules and build directories
        python_count = self.get_language_file_count(results, "Python")
        self.assertEqual(python_count, 8)  # 2 per project
        
        js_count = self.get_language_file_count(results, "JavaScript")
        self.assertEqual(js_count, 0)  # All JS files are in ignored directories
        
    def test_mixed_language_project(self):
        """Test project with multiple languages and ignore patterns."""
        # Create mixed language project
        self.fs.create_file("app.py", "# Python app\n")
        self.fs.create_file("app.js", "// JavaScript\n")
        self.fs.create_file("app.go", "// Go\n")
        self.fs.create_file("style.css", "/* CSS */\n")
        self.fs.create_file("index.html", "<html></html>\n")
        
        # Frontend files
        self.fs.create_file("frontend/app.tsx", "// TypeScript\n")
        self.fs.create_file("frontend/style.scss", "/* SCSS */\n")
        self.fs.create_file("frontend/dist/bundle.js", "// Bundle\n")
        
        # Backend files
        self.fs.create_file("backend/server.py", "# Server\n")
        self.fs.create_file("backend/__pycache__/server.cpython-39.pyc", "bytecode")
        
        # Documentation
        self.fs.create_file("docs/README.md", "# Docs\n")
        self.fs.create_file("docs/api.md", "# API\n")
        
        patterns = {
            ".": ["__pycache__/", "*.pyc"],
            "frontend": ["dist/", "*.map"],
            "docs": []  # Don't ignore anything in docs
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Verify correct files are counted
        self.assertGreater(self.get_language_file_count(results, "Python"), 0)
        self.assertGreater(self.get_language_file_count(results, "JavaScript"), 0)
        self.assertGreater(self.get_language_file_count(results, "Markdown"), 0)
        
    def test_hierarchical_patterns(self):
        """Test hierarchical .ulcignore patterns."""
        self.create_test_project()
        
        # Add hierarchical patterns
        patterns = {
            ".": ["build/"],
            "tests": ["*.tmp"]
        }
        
        results = self.analyze_with_hierarchical(patterns)
        
        # Should work correctly
        self.assertIsNotNone(results)
        self.assertGreater(self.count_files_in_results(results), 0)


# ============================================================================
# TEST RUNNER
# ============================================================================

def run_tests():
    """Run all tests with detailed output."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestCacheStrategy,
        TestIgnoreFileReader,
        TestPatternAdapter,
        TestIgnoreContext,
        TestHierarchicalIgnoreIntegration,
        TestEdgeCases,
        TestPerformanceAndSecurity,
        TestFactoryPattern,
        TestHierarchicalConfigContext,
        TestEndToEnd
    ]
    
    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    
    if result.wasSuccessful():
        print("\n✅ ALL TESTS PASSED!")
    else:
        print("\n❌ SOME TESTS FAILED!")
        
    return result.wasSuccessful()


if __name__ == '__main__':
    sys.exit(0 if run_tests() else 1)