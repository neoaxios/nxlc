# E2E Line Counting Test Framework

## Overview

The E2E (End-to-End) Line Counting Test Framework is a comprehensive testing system designed to validate the accuracy of NXLC's line counting across 400+ programming languages. This framework ensures consistency, prevents regressions, and maintains high quality standards for the line counting tool.

## Architecture

### Core Components

1. **Test Runner** (`test_e2e_line_counting.py`)
   - Main test execution engine
   - Supports parallel and sequential execution
   - Generates detailed reports
   - Platform-agnostic design

2. **Fixture Generator** (`generate_fixtures.py`)
   - Creates standardized test files for each language
   - Generates three fixture types: simple, complex, edge_cases
   - Maintains language-specific syntax rules
   - Extensible template system

3. **Fixture Validator** (`validate_fixtures.py`)
   - Validates fixture structure and consistency
   - Checks for completeness and correctness
   - Performance validation
   - Multi-level severity reporting

4. **Calibration Tool** (`calibrate_fixtures.py`)
   - Synchronizes expected values with actual NXLC output
   - Bulk and individual language calibration
   - Dry-run mode for safe updates

5. **Performance Checker** (`check_performance.py`)
   - Monitors execution time metrics
   - Detects performance regressions
   - Maintains historical baselines
   - Configurable thresholds

## Directory Structure

```
tests/e2e/
├── README.md                          # This documentation
├── test_e2e_line_counting.py         # Main test runner
├── generate_fixtures.py              # Fixture generation tool
├── validate_fixtures.py              # Fixture validation tool
├── calibrate_fixtures.py             # Expected value calibration
├── check_performance.py              # Performance regression checker
├── performance_baseline.json         # Performance metrics baseline
├── test_results.json                 # Latest test results (generated)
└── fixtures/                          # Test fixtures organized by category
    ├── categories.json                # Language metadata and configuration
    ├── common/                        # Most commonly used languages
    │   ├── python/
    │   │   ├── simple.py
    │   │   ├── complex.py
    │   │   ├── edge_cases.py
    │   │   └── expected.json
    │   ├── javascript/
    │   ├── java/
    │   └── ...
    ├── web/                          # Web development languages
    ├── systems/                      # Systems programming languages
    ├── scripting/                    # Scripting languages
    └── ...                           # Additional categories
```

## Quick Start

### Running Tests

```bash
# Run all E2E tests
python3 tests/e2e/test_e2e_line_counting.py

# Run tests for specific category
python3 tests/e2e/test_e2e_line_counting.py --category common

# Run tests for specific language
python3 tests/e2e/test_e2e_line_counting.py --language python --category common

# Verbose output
python3 tests/e2e/test_e2e_line_counting.py --verbose
```

### Adding New Languages

1. **Generate fixtures for a new language:**
```bash
# First, register the language in generate_fixtures.py
# Then generate fixtures
python3 tests/e2e/generate_fixtures.py --language rust
```

2. **Calibrate expected values:**
```bash
python3 tests/e2e/calibrate_fixtures.py --language rust
```

3. **Validate fixtures:**
```bash
python3 tests/e2e/validate_fixtures.py
```

### Maintenance Tasks

#### Validate All Fixtures
```bash
python3 tests/e2e/validate_fixtures.py --strict
```

#### Recalibrate After NXLC Changes
```bash
# Dry run to see what would change
python3 tests/e2e/calibrate_fixtures.py --dry-run

# Apply calibration
python3 tests/e2e/calibrate_fixtures.py
```

#### Check Performance
```bash
python3 tests/e2e/check_performance.py

# Update baseline
python3 tests/e2e/check_performance.py --update
```

## CI/CD Integration

### Git Pre-push Hook

The framework includes a Git pre-push hook that automatically runs tests before allowing pushes:

```bash
# Located at .git/hooks/pre-push
# Automatically installed when setting up the project
```

To bypass (not recommended):
```bash
git push --no-verify
```

### GitHub Actions

The framework includes comprehensive GitHub Actions workflows:

- **Matrix Testing**: Tests across multiple OS and Python versions
- **PR Comments**: Automatic test result summaries on pull requests
- **Performance Tracking**: Historical performance monitoring
- **Scheduled Tests**: Daily comprehensive language coverage tests

## Test Fixture Standards

### Fixture Types

1. **Simple** (5-20 lines)
   - Basic language syntax
   - Single-line comments
   - Multi-line comments (if supported)
   - Simple code structures

2. **Complex** (50-100 lines)
   - Advanced language features
   - Nested structures
   - Mixed code and comments
   - Real-world patterns

3. **Edge Cases** (20-50 lines)
   - Unicode content
   - Comment-like strings
   - Escaped characters
   - Language-specific quirks

### Expected.json Format

```json
{
  "language": "Python",
  "category": "common",
  "extensions": [".py", ".pyw"],
  "simple": {
    "filename": "simple.py",
    "total": 15,
    "code": 8,
    "comments": 5,
    "blank": 2
  },
  "complex": { ... },
  "edge_cases": { ... }
}
```

## Extending the Framework

### Adding a New Language

1. **Register language definition in `generate_fixtures.py`:**
```python
LanguageRegistry.register(LanguageDefinition(
    name="NewLang",
    category="systems",
    extensions=[".nl"],
    comment_style=CommentStyle(
        single_line="//",
        multi_line_start="/*",
        multi_line_end="*/"
    ),
    keywords=["func", "var", "return"]
))
```

2. **Generate and calibrate fixtures:**
```bash
python3 generate_fixtures.py --language newlang
python3 calibrate_fixtures.py --language newlang
```

### Adding Custom Test Strategies

For languages requiring special handling:

```python
class CustomLanguageStrategy(LanguageTestStrategy):
    def prepare_fixture(self, fixture: TestFixture) -> TestFixture:
        # Custom preparation logic
        return fixture
    
    def validate_result(self, fixture: TestFixture, result: TestResult) -> TestResult:
        # Custom validation logic
        return result
    
    def get_tolerance(self) -> float:
        return 0.05  # 5% tolerance

# Register the strategy
TestStrategyFactory.register_strategy("customlang", CustomLanguageStrategy())
```

## Performance Benchmarks

### Target Metrics

- **Per-fixture execution**: < 100ms average
- **Total test suite**: < 30 seconds (parallel)
- **Memory usage**: < 100MB
- **Pass rate**: > 99.5%

### Performance Monitoring

The framework tracks:
- Average execution time per fixture
- Total execution time
- Memory usage patterns
- Historical trends

## Troubleshooting

### Common Issues

1. **Fixture Generation Fails**
   - Check language definition syntax
   - Verify comment style configuration
   - Ensure write permissions

2. **Calibration Mismatches**
   - Verify NXLC is using latest version
   - Check for line ending issues (CRLF vs LF)
   - Ensure fixtures haven't been manually edited

3. **Performance Regressions**
   - Check system load during testing
   - Verify no debug flags are enabled
   - Review recent NXLC changes

4. **Test Failures**
   - Run calibration to sync expected values
   - Check fixture file encoding (should be UTF-8)
   - Validate fixture structure

### Debug Mode

```bash
# Enable debug output
python3 test_e2e_line_counting.py --verbose

# Check specific fixture
python3 -c "
from pathlib import Path
from test_e2e_line_counting import NXLCLineCounter

counter = NXLCLineCounter()
result = counter.count_lines(Path('fixtures/common/python/simple.py'))
print(result)
"
```

## Best Practices

1. **Always validate fixtures after generation**
2. **Run calibration after NXLC updates**
3. **Monitor performance trends**
4. **Add tests for new language features**
5. **Document language-specific quirks**
6. **Use dry-run mode for destructive operations**
7. **Keep fixtures minimal but representative**

## Contributing

### Adding Test Coverage

1. Identify untested languages
2. Create language definition
3. Generate fixtures
4. Calibrate and validate
5. Submit PR with test results

### Improving Accuracy

1. Identify counting discrepancies
2. Add edge case fixtures
3. Update test strategies
4. Document findings

### Performance Optimization

1. Profile slow tests
2. Optimize fixture loading
3. Improve parallel execution
4. Update baselines

## License

This test framework is part of the NXLC project and follows the same license terms.

## Support

For issues or questions:
1. Check this documentation
2. Review existing test fixtures
3. Open an issue with test output
4. Include platform and Python version

---

*Last updated: 2024*
*Framework version: 1.0.0*