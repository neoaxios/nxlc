#!/usr/bin/env python3
"""
Test .nxlcignore functionality
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add parent directory to path to import nxlc
sys.path.insert(0, str(Path(__file__).parent.parent))

import nxlc


class TestUlcIgnore(unittest.TestCase):
    """Test .nxlcignore functionality"""

    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def tearDown(self):
        """Clean up test fixtures"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_nxlcignore_basic(self):
        """Test basic .nxlcignore functionality"""
        # Create test structure
        (self.temp_path / "src").mkdir()
        (self.temp_path / "test").mkdir()
        (self.temp_path / "node_modules").mkdir()
        
        # Create test files
        (self.temp_path / "main.py").write_text("print('main')")
        (self.temp_path / "src" / "app.py").write_text("print('app')")
        (self.temp_path / "test" / "test_app.py").write_text("print('test')")
        (self.temp_path / "node_modules" / "lib.js").write_text("console.log('lib');")
        
        # Create .nxlcignore file
        nxlcignore_content = """# Ignore node_modules
node_modules/
# Ignore test directory
test/
"""
        (self.temp_path / ".nxlcignore").write_text(nxlcignore_content)
        
        # Run analysis
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Verify results
        self.assertTrue(results['using_nxlcignore'])
        # Should only find Python files (main.py and src/app.py)
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        # JavaScript from node_modules should be ignored
        self.assertNotIn('JavaScript', results['languages'])
        
    def test_nxlcignore_patterns(self):
        """Test various .nxlcignore patterns"""
        # Create test files
        (self.temp_path / "script.py").write_text("print('hello')")
        (self.temp_path / "data.csv").write_text("a,b,c")
        (self.temp_path / "build.log").write_text("build output")
        (self.temp_path / "app.min.js").write_text("minified")
        (self.temp_path / "app.js").write_text("console.log('app');")
        
        # Create .nxlcignore with patterns
        nxlcignore_content = """# Ignore specific extensions
*.csv
*.log
# Ignore minified files
*.min.js
"""
        (self.temp_path / ".nxlcignore").write_text(nxlcignore_content)
        
        # Run analysis
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should find script.py and app.js, but not csv, log, or min.js
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        self.assertIn('JavaScript', results['languages'])
        
    def test_nxlcignore_with_gitignore(self):
        """Test .nxlcignore working alongside .gitignore"""
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
        
        # Create .nxlcignore (ignores temp/)
        (self.temp_path / ".nxlcignore").write_text("temp/\n")
        
        # Run analysis with git enabled
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should find src/main.py and .gitignore (configuration file)
        # dist/ ignored by .gitignore, temp/ ignored by .nxlcignore
        self.assertEqual(results['total_files'], 2)  # main.py + .gitignore
        self.assertIn('Python', results['languages'])
        self.assertIn('Configuration', results['languages'])  # .gitignore is a config file
        self.assertTrue(results['using_git'])
        self.assertTrue(results['using_nxlcignore'])
        
    def test_nxlcignore_subdirectory_patterns(self):
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
        
        # Create .nxlcignore with directory pattern
        (self.temp_path / ".nxlcignore").write_text("**/test_data/\n")
        
        # Run analysis
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should only find the .py files, not the test_data contents
        self.assertEqual(results['total_files'], 2)
        self.assertIn('Python', results['languages'])
        self.assertNotIn('JSON', results['languages'])
        self.assertNotIn('Text', results['languages'])
        
    def test_empty_nxlcignore(self):
        """Test that empty .nxlcignore file doesn't break anything"""
        # Create test file
        (self.temp_path / "test.py").write_text("print('test')")
        
        # Create empty .nxlcignore
        (self.temp_path / ".nxlcignore").write_text("")
        
        # Run analysis
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should work normally
        self.assertEqual(results['total_files'], 1)
        self.assertIn('Python', results['languages'])
        # Empty .nxlcignore still counts as "using" since the file exists
        self.assertTrue(results['using_nxlcignore'])
        
    def test_nxlcignore_with_comments(self):
        """Test .nxlcignore with comments and blank lines"""
        # Create test files
        (self.temp_path / "app.py").write_text("print('app')")
        (self.temp_path / "test.txt").write_text("test")
        (self.temp_path / "data.csv").write_text("a,b,c")
        
        # Create .nxlcignore with comments and blank lines
        nxlcignore_content = """# This is a comment
# Another comment

# Ignore CSV files
*.csv

# Ignore text files
*.txt
# End of file
"""
        (self.temp_path / ".nxlcignore").write_text(nxlcignore_content)
        
        # Run analysis
        counter = nxlc.LineCounter()
        results = counter.analyze_directory(self.temp_path)
        
        # Should only find app.py
        self.assertEqual(results['total_files'], 1)
        self.assertIn('Python', results['languages'])


if __name__ == "__main__":
    unittest.main()