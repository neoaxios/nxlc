#!/usr/bin/env python3
"""
Test .ulcignore functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import ulc
sys.path.insert(0, str(Path(__file__).parent.parent))

import ulc


class TestUlcIgnore(unittest.TestCase):
    """Test .ulcignore functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_ulcignore_basic(self):
        """Test basic .ulcignore functionality"""
        # Create test structure
        (self.temp_path / "src").mkdir()
        (self.temp_path / "test").mkdir()
        (self.temp_path / "node_modules").mkdir()
        
        # Create test files
        (self.temp_path / "main.py").write_text("print('main')")
        (self.temp_path / "src" / "app.py").write_text("print('app')")
        (self.temp_path / "test" / "test_app.py").write_text("print('test')")
        (self.temp_path / "node_modules" / "lib.js").write_text("console.log('lib');")
        
        # Create .ulcignore file
        ulcignore_content = """# Ignore node_modules
node_modules/
# Ignore test directory
test/
"""
        (self.temp_path / ".ulcignore").write_text(ulcignore_content)
        
        # Run analysis
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Verify results
        self.assertTrue(results['using_ulcignore'])
        # Should only find Python files (main.py and src/app.py)
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        # JavaScript from node_modules should be ignored
        self.assertNotIn('JavaScript', results['languages'])
        
    def test_ulcignore_patterns(self):
        """Test various .ulcignore patterns"""
        # Create test files
        (self.temp_path / "script.py").write_text("print('hello')")
        (self.temp_path / "data.csv").write_text("a,b,c")
        (self.temp_path / "build.log").write_text("build output")
        (self.temp_path / "app.min.js").write_text("minified")
        (self.temp_path / "app.js").write_text("console.log('app');")
        
        # Create .ulcignore with patterns
        ulcignore_content = """# Ignore specific extensions
*.csv
*.log
# Ignore minified files
*.min.js
"""
        (self.temp_path / ".ulcignore").write_text(ulcignore_content)
        
        # Run analysis
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should find script.py and app.js, but not csv, log, or min.js
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        self.assertIn('JavaScript', results['languages'])
        
    def test_ulcignore_with_gitignore(self):
        """Test .ulcignore working alongside .gitignore"""
        # Create git structure
        (self.temp_path / ".git").mkdir()  # Make it a git repo
        (self.temp_path / "src").mkdir()
        (self.temp_path / "dist").mkdir()
        (self.temp_path / "temp").mkdir()
        
        # Create files
        (self.temp_path / "src" / "main.py").write_text("print('main')")
        (self.temp_path / "dist" / "bundle.js").write_text("bundled")
        (self.temp_path / "temp" / "cache.txt").write_text("cache")
        
        # Create .gitignore (ignores dist/)
        (self.temp_path / ".gitignore").write_text("dist/\n")
        
        # Create .ulcignore (ignores temp/)
        (self.temp_path / ".ulcignore").write_text("temp/\n")
        
        # Run analysis with git enabled
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should find src/main.py and .gitignore (configuration file)
        # dist/ ignored by .gitignore, temp/ ignored by .ulcignore
        self.assertEqual(results['total_files'], 2)  # main.py + .gitignore
        self.assertIn('Python', results['languages'])
        self.assertIn('Configuration', results['languages'])  # .gitignore is a config file
        self.assertTrue(results['using_git'])
        self.assertTrue(results['using_ulcignore'])
        
    def test_ulcignore_subdirectory_patterns(self):
        """Test patterns that match in subdirectories"""
        # Create nested structure
        (self.temp_path / "src").mkdir()
        (self.temp_path / "src" / "test_data").mkdir()
        (self.temp_path / "lib").mkdir()
        (self.temp_path / "lib" / "test_data").mkdir()
        
        # Create files
        (self.temp_path / "src" / "app.py").write_text("print('app')")
        (self.temp_path / "src" / "test_data" / "sample.txt").write_text("data")
        (self.temp_path / "lib" / "util.py").write_text("print('util')")
        (self.temp_path / "lib" / "test_data" / "fixture.json").write_text("{}")
        
        # Create .ulcignore with directory pattern
        (self.temp_path / ".ulcignore").write_text("**/test_data/\n")
        
        # Run analysis
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should only find the .py files, not the test_data contents
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        self.assertNotIn('JSON', results['languages'])
        self.assertNotIn('Text', results['languages'])
        
    def test_empty_ulcignore(self):
        """Test that empty .ulcignore file doesn't break anything"""
        # Create test file
        (self.temp_path / "test.py").write_text("print('test')")
        
        # Create empty .ulcignore
        (self.temp_path / ".ulcignore").write_text("")
        
        # Run analysis
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should work normally
        self.assertEqual(results['total_files'], 1)
        self.assertIn('Python', results['languages'])
        # Empty .ulcignore doesn't count as "using"
        self.assertFalse(results['using_ulcignore'])
        
    def test_ulcignore_with_comments(self):
        """Test .ulcignore with comments and blank lines"""
        # Create test files
        (self.temp_path / "app.py").write_text("print('app')")
        (self.temp_path / "test.txt").write_text("test")
        (self.temp_path / "data.csv").write_text("a,b,c")
        
        # Create .ulcignore with comments and blank lines
        ulcignore_content = """# This is a comment
# Another comment

# Ignore CSV files
*.csv

# Ignore text files
*.txt
# End of file
"""
        (self.temp_path / ".ulcignore").write_text(ulcignore_content)
        
        # Run analysis
        counter = ulc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should only find app.py
        self.assertEqual(results['total_files'], 1)
        self.assertIn('Python', results['languages'])


if __name__ == "__main__":
    unittest.main()