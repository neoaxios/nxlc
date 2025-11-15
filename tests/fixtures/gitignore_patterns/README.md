# GitIgnore Pattern Test Fixtures

This directory contains reusable test fixtures for validating .gitignore pattern handling,
specifically focusing on directory patterns with trailing slashes.

## Purpose

These fixtures validate that nxlc correctly respects .gitignore patterns, matching git's
behavior for directory patterns.

## Bug Context

**Issue**: Files inside directories with .gitignore patterns ending in `/` were being counted.

**Example**:
```
# .gitignore
.testgrid-cache/
```

Before fix: Files in `.testgrid-cache/` were incorrectly counted
After fix: Files in `.testgrid-cache/` are correctly ignored

## Test Fixtures

### 1. Basic Directory Pattern (`basic_dir_pattern/`)

Tests that a simple directory pattern ignores all files in that directory.

**Structure**:
```
basic_dir_pattern/
├── .git/
├── .gitignore          # Contains: .testgrid-cache/
├── .testgrid-cache/
│   ├── data.json       # Should be IGNORED
│   └── results.txt     # Should be IGNORED
├── main.py             # Should be counted
└── README.md           # Should be counted
```

**Expected**: 3 files (main.py, README.md, .gitignore)

### 2. Nested Directory Pattern (`nested_dir_pattern/`)

Tests that nested files within ignored directories are also ignored.

**Structure**:
```
nested_dir_pattern/
├── .git/
├── .gitignore                      # Contains: .llmreplay_cache/
├── .llmreplay_cache/
│   ├── session1/
│   │   ├── data.json              # Should be IGNORED
│   │   └── logs/debug.log         # Should be IGNORED
│   └── session2/
│       ├── data.json              # Should be IGNORED
│       └── logs/debug.log         # Should be IGNORED
└── config.json                     # Should be counted
```

**Expected**: 2 files (config.json, .gitignore)

### 3. Multiple Directory Patterns (`multi_dir_patterns/`)

Tests multiple directory patterns in a single .gitignore file.

**Structure**:
```
multi_dir_patterns/
├── .git/
├── .gitignore                      # Contains multiple patterns
├── .testgrid-cache/data.txt        # Should be IGNORED
├── .build-cache/output.txt         # Should be IGNORED
├── .llmreplay_cache/replay.txt     # Should be IGNORED
├── node_modules/lib.js             # Should be IGNORED
└── main.py                         # Should be counted
```

**Expected**: 2 files (main.py, .gitignore)

### 4. Real World Bug Case (`real_world_bug/`)

Recreates the exact bug scenario from production usage.

**Structure**:
```
real_world_bug/
├── .git/
├── .gitignore                          # Contains: .testgrid-cache/
├── .testgrid-cache/
│   ├── 2024-01-15_run1.json           # Should be IGNORED
│   ├── 2024-01-15_run2.json           # Should be IGNORED
│   └── metadata.txt                   # Should be IGNORED
├── src/main.py                         # Should be counted
├── tests/test_main.py                  # Should be counted
└── README.md                           # Should be counted
```

**Expected**: 4 files (src/main.py, tests/test_main.py, README.md, .gitignore)

## Usage

These fixtures can be used in tests like this:

```python
import tempfile
import shutil
from pathlib import Path

def test_using_fixture():
    # Copy fixture to temp directory
    fixture_dir = Path(__file__).parent / "fixtures" / "gitignore_patterns" / "basic_dir_pattern"
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)
        shutil.copytree(fixture_dir, temp_path / "test", dirs_exist_ok=True)

        # Run nxlc analysis
        from nxlc import LineCounter
        counter = LineCounter()
        results = counter.analyze_directory(temp_path / "test")

        # Verify results
        assert results['total_files'] == 3  # Expected count from fixture
```

## Verification

To verify a fixture is set up correctly, you can use git itself:

```bash
cd fixtures/gitignore_patterns/basic_dir_pattern
git ls-files --others --ignored --exclude-standard
```

This should show the files that git would ignore, matching what nxlc should ignore.

## File Contents

All files contain minimal content to be recognizable:
- Python files: `print('filename')`
- JSON files: `{}`
- Text files: "test data"
- Markdown files: `# Filename`

## Notes

- Each fixture includes a `.git/` directory to simulate a git repository
- All .gitignore files use Unix line endings (LF)
- Patterns are tested as-is without negation or complex glob patterns
- Focus is on directory patterns ending with `/`
