#!/usr/bin/env python3
"""
Test .gitignore handling using reusable fixtures.

This test suite uses pre-built fixtures to validate that nxlc correctly
handles .gitignore patterns, specifically directory patterns ending with `/`.
"""

import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
from typing import Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import nxlc


class GitIgnoreFixtureTestBase(unittest.TestCase):
    """Base class for .gitignore fixture-based tests."""

    @classmethod
    def setUpClass(cls):
        """Set up class-level resources."""
        cls.fixtures_dir = Path(__file__).parent / 'fixtures' / 'gitignore_patterns'
        cls.counter = nxlc.LineCounter()

    def setUp(self):
        """Set up test environment with temp directory."""
        self.test_dir = tempfile.mkdtemp(prefix="nxlc_fixture_test_")
        self.test_path = Path(self.test_dir)

    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def load_fixture(self, fixture_name: str) -> Path:
        """
        Load a fixture into the test directory.

        Args:
            fixture_name: Name of fixture directory to load

        Returns:
            Path to the loaded fixture in test directory
        """
        fixture_source = self.fixtures_dir / fixture_name
        if not fixture_source.exists():
            raise FileNotFoundError(f"Fixture not found: {fixture_source}")

        # Copy fixture to test directory
        fixture_dest = self.test_path / fixture_name
        shutil.copytree(fixture_source, fixture_dest)

        return fixture_dest

    def analyze_fixture(self, fixture_path: Path, verbose: bool = False) -> Dict[str, Any]:
        """
        Analyze a fixture using nxlc.

        Args:
            fixture_path: Path to fixture directory
            verbose: Enable verbose output

        Returns:
            Analysis results dictionary
        """
        return self.counter.analyze_directory(
            directory=fixture_path,
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


class TestBasicDirectoryPattern(GitIgnoreFixtureTestBase):
    """Test basic directory pattern fixture."""

    def test_basic_dir_pattern_ignores_directory_files(self):
        """Test that basic directory pattern ignores all files in directory."""
        # Load fixture
        fixture = self.load_fixture('basic_dir_pattern')

        # Analyze
        results = self.analyze_fixture(fixture)

        # Verify: Should find main.py, README.md, .gitignore (3 files)
        # Should NOT find .testgrid-cache/data.json or .testgrid-cache/results.txt
        self.assertEqual(
            self.get_file_count(results), 3,
            f"Expected 3 files, got {self.get_file_count(results)}. "
            f"Files should be: main.py, README.md, .gitignore"
        )

        # Verify specific languages
        self.assertEqual(self.get_language_file_count(results, "Python"), 1, "Should find main.py")
        self.assertEqual(self.get_language_file_count(results, "README"), 1, "Should find README.md")  # README.md is detected as README
        self.assertEqual(self.get_language_file_count(results, "JSON"), 0, "Should NOT find data.json")
        self.assertEqual(self.get_language_file_count(results, "Text"), 0, "Should NOT find results.txt")


class TestNestedDirectoryPattern(GitIgnoreFixtureTestBase):
    """Test nested directory pattern fixture."""

    def test_nested_dir_pattern_ignores_all_nested_files(self):
        """Test that nested files within ignored directories are also ignored."""
        # Load fixture
        fixture = self.load_fixture('nested_dir_pattern')

        # Analyze
        results = self.analyze_fixture(fixture)

        # Verify: Should find config.json, .gitignore (2 files)
        # Should NOT find any files in .llmreplay_cache/
        self.assertEqual(
            self.get_file_count(results), 2,
            f"Expected 2 files, got {self.get_file_count(results)}. "
            f"All files in .llmreplay_cache/ should be ignored"
        )

        # Verify specific languages
        self.assertEqual(self.get_language_file_count(results, "JSON"), 1, "Should find config.json only")


class TestMultipleDirectoryPatterns(GitIgnoreFixtureTestBase):
    """Test multiple directory patterns fixture."""

    def test_multi_dir_patterns_ignore_all_specified_directories(self):
        """Test that multiple directory patterns all work correctly."""
        # Load fixture
        fixture = self.load_fixture('multi_dir_patterns')

        # Analyze
        results = self.analyze_fixture(fixture)

        # Verify: Should find main.py, .gitignore (2 files)
        # Should NOT find files in any cache directory or node_modules
        self.assertEqual(
            self.get_file_count(results), 2,
            f"Expected 2 files, got {self.get_file_count(results)}. "
            f"All cache directories should be ignored"
        )

        # Verify specific languages
        self.assertEqual(self.get_language_file_count(results, "Python"), 1, "Should find main.py")
        self.assertEqual(self.get_language_file_count(results, "Text"), 0, "Should NOT find any .txt files")
        self.assertEqual(self.get_language_file_count(results, "JavaScript"), 0, "Should NOT find lib.js")


class TestRealWorldBug(GitIgnoreFixtureTestBase):
    """Test real-world bug case fixture."""

    def test_real_world_bug_testgrid_cache_ignored(self):
        """Test the exact bug scenario: .testgrid-cache/ files should be ignored."""
        # Load fixture
        fixture = self.load_fixture('real_world_bug')

        # Analyze
        results = self.analyze_fixture(fixture)

        # Verify: Should find src/main.py, tests/test_main.py, README.md, .gitignore (4 files)
        # Should NOT find any files in .testgrid-cache/
        self.assertEqual(
            self.get_file_count(results), 4,
            f"Expected 4 files, got {self.get_file_count(results)}. "
            f"Files in .testgrid-cache/ should be ignored"
        )

        # Verify specific languages
        self.assertEqual(
            self.get_language_file_count(results, "JSON"), 0,
            "Should NOT find any JSON files (.testgrid-cache/ should be ignored)"
        )
        self.assertEqual(
            self.get_language_file_count(results, "Python"), 2,
            "Should find src/main.py and tests/test_main.py"
        )
        self.assertEqual(
            self.get_language_file_count(results, "README"), 1,  # README.md is detected as README
            "Should find README.md"
        )


class TestFixtureVerboseOutput(GitIgnoreFixtureTestBase):
    """Test verbose output with fixtures."""

    def test_verbose_output_does_not_show_ignored_files(self):
        """Test that verbose mode doesn't show files in ignored directories."""
        # Load fixture
        fixture = self.load_fixture('basic_dir_pattern')

        # Analyze with verbose
        results = self.analyze_fixture(fixture, verbose=True)

        # Verify file count is still correct
        self.assertEqual(self.get_file_count(results), 3)


def run_tests():
    """Run all fixture-based tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    test_classes = [
        TestBasicDirectoryPattern,
        TestNestedDirectoryPattern,
        TestMultipleDirectoryPatterns,
        TestRealWorldBug,
        TestFixtureVerboseOutput
    ]

    for test_class in test_classes:
        suite.addTests(loader.loadTestsFromTestCase(test_class))

    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY: .gitignore Fixture Tests")
    print("="*70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")

    if result.wasSuccessful():
        print("\nALL TESTS PASSED")
        print("\nThese tests validate the .gitignore directory pattern fix.")
        print("Before fix: Files in directories with trailing / were counted")
        print("After fix: Files in these directories are correctly ignored")
    else:
        print("\nSOME TESTS FAILED")
        print("\nThis indicates the .gitignore directory pattern bug still exists.")
        if result.failures:
            print("\nFailed tests show where directory patterns are not working correctly.")

    return result.wasSuccessful()


if __name__ == '__main__':
    sys.exit(0 if run_tests() else 1)
