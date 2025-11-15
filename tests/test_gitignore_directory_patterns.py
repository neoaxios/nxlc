#!/usr/bin/env python3
"""
E2E Test Suite for .gitignore Directory Pattern Fix

Tests that nxlc correctly handles .gitignore patterns ending with `/`
(directory patterns) and ignores all files within those directories.

Bug context:
- Patterns like `.testgrid-cache/` should ignore ALL files in that directory
- Files inside ignored directories should NOT be counted
- Behavior should match git's .gitignore semantics
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
from typing import Dict, Any, List

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import nxlc


class GitIgnoreDirectoryPatternTestBase(unittest.TestCase):
    """Base class providing test infrastructure for .gitignore directory pattern tests."""

    def setUp(self):
        """Set up test environment with temp directory."""
        self.test_dir = tempfile.mkdtemp(prefix="nxlc_gitignore_test_")
        self.test_path = Path(self.test_dir)
        self.counter = nxlc.LineCounter()

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def create_file(self, relative_path: str, content: str = "") -> Path:
        """Create a file with given content."""
        full_path = self.test_path / relative_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content)
        return full_path

    def create_git_repo(self) -> Path:
        """Create a .git directory to make this a git repository."""
        git_dir = self.test_path / ".git"
        git_dir.mkdir(parents=True, exist_ok=True)
        return git_dir

    def create_gitignore(self, patterns: List[str]) -> Path:
        """Create a .gitignore file with given patterns."""
        content = "\n".join(patterns)
        return self.create_file(".gitignore", content)

    def analyze_directory(self, verbose: bool = False) -> Dict[str, Any]:
        """Analyze the test directory using nxlc."""
        return self.counter.analyze_directory(
            directory=self.test_path,
            verbose=verbose,
            debug=False
        )

    def get_file_count(self, results: Dict[str, Any]) -> int:
        """Get total file count from results."""
        return results.get('total_files', 0)

    def get_language_file_count(self, results: Dict[str, Any], language: str) -> int:
        """Get file count for a specific language."""
        languages = results.get('languages', {})
        if language in languages:
            return languages[language].get('files', 0)
        return 0


class TestDirectoryPatternBasics(GitIgnoreDirectoryPatternTestBase):
    """Test basic directory pattern functionality."""

    def test_directory_pattern_with_trailing_slash(self):
        """Test that directory patterns with trailing / ignore all files in that directory."""
        # Create git repo
        self.create_git_repo()

        # Create cache directory with files
        self.create_file(".testgrid-cache/data.json", '{"test": "data"}')
        self.create_file(".testgrid-cache/results.txt", "test results")
        self.create_file(".testgrid-cache/report.md", "# Report")

        # Create non-ignored files
        self.create_file("main.py", "print('main')")
        self.create_file("README.md", "# README")

        # Create .gitignore with directory pattern
        self.create_gitignore([".testgrid-cache/"])

        # Analyze
        results = self.analyze_directory()

        # Should find main.py, README.md, and .gitignore (3 files)
        # Should NOT find any files in .testgrid-cache/
        self.assertEqual(self.get_file_count(results), 3)
        self.assertEqual(self.get_language_file_count(results, "Python"), 1)
        self.assertEqual(self.get_language_file_count(results, "README"), 1)  # README.md is detected as README, not Markdown
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0)
        self.assertEqual(self.get_language_file_count(results, "Text"), 0)

    def test_directory_pattern_without_trailing_slash(self):
        """Test that directory patterns without trailing / also work correctly."""
        self.create_git_repo()

        # Create cache directory with files
        self.create_file(".build-cache/output.js", "console.log('built');")
        self.create_file(".build-cache/bundle.min.js", "minified")

        # Create non-ignored files
        self.create_file("app.js", "console.log('app');")

        # Create .gitignore with directory pattern (without trailing /)
        self.create_gitignore([".build-cache"])

        # Analyze
        results = self.analyze_directory()

        # Should find app.js and .gitignore only
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "JavaScript"), 1)

    def test_nested_files_in_ignored_directory(self):
        """Test that nested files within ignored directories are also ignored."""
        self.create_git_repo()

        # Create nested structure in ignored directory
        self.create_file(".llmreplay_cache/session1/data.json", '{}')
        self.create_file(".llmreplay_cache/session1/logs/debug.log", "log")
        self.create_file(".llmreplay_cache/session2/data.json", '{}')
        self.create_file(".llmreplay_cache/session2/logs/debug.log", "log")

        # Create non-ignored files
        self.create_file("config.json", '{"key": "value"}')

        # Create .gitignore
        self.create_gitignore([".llmreplay_cache/"])

        # Analyze
        results = self.analyze_directory()

        # Should only find config.json and .gitignore
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "JSON"), 1)

    def test_multiple_directory_patterns(self):
        """Test multiple directory patterns in .gitignore."""
        self.create_git_repo()

        # Create multiple cache directories
        self.create_file(".testgrid-cache/data.txt", "test")
        self.create_file(".build-cache/output.txt", "build")
        self.create_file(".llmreplay_cache/replay.txt", "replay")
        self.create_file("node_modules/lib.js", "library")

        # Create non-ignored files
        self.create_file("main.py", "print('main')")

        # Create .gitignore with multiple directory patterns
        self.create_gitignore([
            ".testgrid-cache/",
            ".build-cache/",
            ".llmreplay_cache/",
            "node_modules/"
        ])

        # Analyze
        results = self.analyze_directory()

        # Should only find main.py and .gitignore
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "Python"), 1)
        self.assertEqual(self.get_language_file_count(results, "Text"), 0)
        self.assertEqual(self.get_language_file_count(results, "JavaScript"), 0)


class TestDirectoryPatternEdgeCases(GitIgnoreDirectoryPatternTestBase):
    """Test edge cases for directory patterns."""

    def test_directory_pattern_with_similar_names(self):
        """Test that directory patterns don't match similar file names."""
        self.create_git_repo()

        # Create directory and similar file
        self.create_file("cache/data.txt", "cache dir")
        self.create_file("cache.txt", "cache file")

        # Ignore directory only
        self.create_gitignore(["cache/"])

        # Analyze
        results = self.analyze_directory()

        # Should find cache.txt and .gitignore, but not cache/data.txt
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "Text"), 1)

    def test_directory_pattern_case_sensitivity(self):
        """Test case sensitivity of directory patterns."""
        self.create_git_repo()

        # Create directories with different cases
        self.create_file("Cache/data.txt", "upper")
        self.create_file("cache/data.txt", "lower")

        # Ignore lowercase version
        self.create_gitignore(["cache/"])

        # Analyze
        results = self.analyze_directory()

        # On case-sensitive systems, Cache/ should not be ignored
        # On case-insensitive systems (Windows), both might be ignored
        import platform
        if platform.system() == 'Windows':
            # Windows is case-insensitive
            self.assertLessEqual(self.get_file_count(results), 2)  # At most .gitignore
        else:
            # Unix-like systems are case-sensitive
            self.assertEqual(self.get_file_count(results), 2)  # Cache/data.txt + .gitignore

    def test_empty_directory_pattern(self):
        """Test that empty directories don't cause issues."""
        self.create_git_repo()

        # Create empty ignored directory
        (self.test_path / "empty_cache").mkdir(parents=True, exist_ok=True)

        # Create non-empty directory
        self.create_file("src/main.py", "print('main')")

        # Ignore empty directory
        self.create_gitignore(["empty_cache/"])

        # Analyze
        results = self.analyze_directory()

        # Should find src/main.py and .gitignore
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "Python"), 1)

    def test_deeply_nested_ignored_directory(self):
        """Test deeply nested directory patterns."""
        self.create_git_repo()

        # Create deeply nested structure
        self.create_file("project/src/cache/level1/level2/level3/data.json", '{}')
        self.create_file("project/src/main.py", "print('main')")

        # Ignore cache at any level using glob pattern
        self.create_gitignore(["**/cache/"])

        # Analyze
        results = self.analyze_directory()

        # Should find main.py and .gitignore, but not data.json in cache
        self.assertEqual(self.get_file_count(results), 2)
        self.assertEqual(self.get_language_file_count(results, "Python"), 1)
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0)


class TestDirectoryPatternWithComments(GitIgnoreDirectoryPatternTestBase):
    """Test .gitignore files with comments and formatting."""

    def test_gitignore_with_comments(self):
        """Test that comments in .gitignore are properly handled."""
        self.create_git_repo()

        # Create test files
        self.create_file(".testgrid-cache/data.txt", "test")
        self.create_file("main.py", "print('main')")

        # Create .gitignore with comments
        gitignore_content = """# This is a comment
# Ignore test cache directories
.testgrid-cache/

# Another comment
# More patterns could go here
"""
        self.create_file(".gitignore", gitignore_content)

        # Analyze
        results = self.analyze_directory()

        # Should ignore cache directory
        self.assertEqual(self.get_file_count(results), 2)  # main.py + .gitignore
        self.assertEqual(self.get_language_file_count(results, "Text"), 0)

    def test_gitignore_with_blank_lines(self):
        """Test that blank lines in .gitignore don't cause issues."""
        self.create_git_repo()

        # Create test files
        self.create_file(".build-cache/output.txt", "build")
        self.create_file("app.py", "print('app')")

        # Create .gitignore with blank lines
        gitignore_content = """
.build-cache/

"""
        self.create_file(".gitignore", gitignore_content)

        # Analyze
        results = self.analyze_directory()

        # Should ignore cache directory
        self.assertEqual(self.get_file_count(results), 2)  # app.py + .gitignore


class TestVerboseOutput(GitIgnoreDirectoryPatternTestBase):
    """Test verbose output doesn't show ignored files."""

    def test_verbose_output_excludes_ignored_files(self):
        """Test that verbose mode doesn't show files in ignored directories."""
        self.create_git_repo()

        # Create ignored and non-ignored files
        self.create_file(".testgrid-cache/data.json", '{}')
        self.create_file("main.py", "print('main')")

        # Create .gitignore
        self.create_gitignore([".testgrid-cache/"])

        # Analyze with verbose mode
        results = self.analyze_directory(verbose=True)

        # Verify files are correctly ignored
        self.assertEqual(self.get_file_count(results), 2)  # main.py + .gitignore
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0)


class TestGitModeToggle(GitIgnoreDirectoryPatternTestBase):
    """Test git mode can be toggled on/off."""

    def test_no_git_flag_disables_gitignore(self):
        """Test that --no-git flag disables .gitignore processing."""
        self.create_git_repo()

        # Create files
        self.create_file(".testgrid-cache/data.txt", "test")
        self.create_file("main.py", "print('main')")

        # Create .gitignore
        self.create_gitignore([".testgrid-cache/"])

        # Analyze with no_git=True
        results = self.counter.analyze_directory(
            directory=self.test_path,
            no_git=True
        )

        # Should count all files when git mode is disabled
        # .gitignore, main.py, and .testgrid-cache/data.txt
        self.assertGreaterEqual(self.get_file_count(results), 3)

    def test_git_flag_enables_gitignore_in_non_git_dir(self):
        """Test that --git flag enables .gitignore processing in non-git directories."""
        # Don't create .git directory

        # Create files
        self.create_file(".testgrid-cache/data.txt", "test")
        self.create_file("main.py", "print('main')")

        # Create .gitignore
        self.create_gitignore([".testgrid-cache/"])

        # Analyze with use_git=True
        results = self.counter.analyze_directory(
            directory=self.test_path,
            use_git=True
        )

        # Should respect .gitignore even in non-git directory
        self.assertEqual(self.get_file_count(results), 2)  # main.py + .gitignore
        self.assertEqual(self.get_language_file_count(results, "Text"), 0)


class TestRealWorldScenarios(GitIgnoreDirectoryPatternTestBase):
    """Test real-world scenarios from actual usage."""

    def test_bug_testgrid_cache(self):
        """Test the specific bug case: .testgrid-cache/ files were being counted."""
        self.create_git_repo()

        # Recreate the bug scenario
        self.create_file(".testgrid-cache/2024-01-15_run1.json", '{}')
        self.create_file(".testgrid-cache/2024-01-15_run2.json", '{}')
        self.create_file(".testgrid-cache/metadata.txt", "metadata")

        # Create project files
        self.create_file("src/main.py", "print('main')")
        self.create_file("tests/test_main.py", "def test(): pass")
        self.create_file("README.md", "# Project")

        # Create .gitignore with cache pattern
        self.create_gitignore([".testgrid-cache/"])

        # Analyze
        results = self.analyze_directory()

        # Before fix: would count .testgrid-cache files
        # After fix: should NOT count .testgrid-cache files
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0)
        self.assertEqual(self.get_language_file_count(results, "Python"), 2)
        self.assertEqual(self.get_language_file_count(results, "README"), 1)  # README.md is detected as README, not Markdown

    def test_bug_multiple_cache_directories(self):
        """Test multiple cache directories as seen in real usage."""
        self.create_git_repo()

        # Create multiple cache directories
        self.create_file(".testgrid-cache/test1.json", '{}')
        self.create_file(".build-cache/build1.txt", "build")
        self.create_file(".llmreplay_cache/replay1.log", "log")

        # Create project files
        self.create_file("main.py", "print('main')")

        # Create .gitignore
        self.create_gitignore([
            ".testgrid-cache/",
            ".build-cache/",
            ".llmreplay_cache/"
        ])

        # Analyze
        results = self.analyze_directory()

        # Should only count project files
        self.assertEqual(self.get_file_count(results), 2)  # main.py + .gitignore
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0)
        self.assertEqual(self.get_language_file_count(results, "Text"), 0)

    def test_common_cache_patterns(self):
        """Test common cache and build directory patterns."""
        self.create_git_repo()

        # Create common cache/build directories
        self.create_file("node_modules/package/index.js", "exports = {};")
        self.create_file("__pycache__/module.cpython-39.pyc", "bytecode")
        self.create_file(".pytest_cache/cache.json", "{}")
        self.create_file("build/output.js", "built")
        self.create_file("dist/bundle.min.js", "minified")

        # Create project files
        self.create_file("src/main.py", "print('main')")

        # Create .gitignore with common patterns
        self.create_gitignore([
            "node_modules/",
            "__pycache__/",
            ".pytest_cache/",
            "build/",
            "dist/"
        ])

        # Analyze
        results = self.analyze_directory()

        # Should only count project files
        self.assertEqual(self.get_file_count(results), 2)  # main.py + .gitignore
        self.assertEqual(self.get_language_file_count(results, "Python"), 1)
        self.assertEqual(self.get_language_file_count(results, "JavaScript"), 0)


def run_tests():
    """Run all tests with detailed output."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestDirectoryPatternBasics,
        TestDirectoryPatternEdgeCases,
        TestDirectoryPatternWithComments,
        TestVerboseOutput,
        TestGitModeToggle,
        TestRealWorldScenarios
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY: .gitignore Directory Pattern Tests")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")

    if result.wasSuccessful():
        print("\nALL TESTS PASSED")
    else:
        print("\nSOME TESTS FAILED")
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}")
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}")

    return result.wasSuccessful()


if __name__ == '__main__':
    sys.exit(0 if run_tests() else 1)
