# Contributing to Universal Language Counter (ULC)

Thank you for your interest in contributing to ULC! This document provides guidelines and instructions for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Issues

- Check existing issues first to avoid duplicates
- Use issue templates when available
- Include system information (OS, Python version)
- Provide minimal reproducible examples
- Include relevant error messages and logs

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the use case and benefits
- Consider implementation complexity
- Be open to discussion and alternatives

### Submitting Changes

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation as needed
   - Keep commits focused and atomic

4. **Test your changes**
   ```bash
   python -m pytest tests/
   python ulc.py .  # Manual testing
   ```

5. **Submit a Pull Request**
   - Reference related issues
   - Describe what changed and why
   - Include test results
   - Be responsive to feedback

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ulc.git
cd ulc

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

## Code Style

- Follow PEP 8 guidelines
- Use meaningful variable names
- Add type hints where appropriate
- Document complex logic with comments
- Maximum line length: 100 characters

## Testing

- Write tests for new features
- Maintain or improve code coverage
- Test edge cases and error conditions
- Run tests before submitting PR:
  ```bash
  pytest tests/ -v
  ```

## Adding Language Support

To add support for a new programming language:

1. Add language definition to `LANGUAGE_EXTENSIONS` in `ulc.py`
2. Handle any special comment syntax in language definitions
3. Add test files in `tests/test_files/`
4. Update README.md supported languages list
5. Add tests to verify correct counting

## Documentation

- Update README.md for user-facing changes
- Add docstrings to new functions/classes
- Update CHANGELOG.md with notable changes
- Include examples for new features

## Pull Request Process

1. Ensure all tests pass
2. Update documentation
3. Add entry to CHANGELOG.md
4. Request review from maintainers
5. Address feedback promptly
6. Squash commits if requested

## Questions?

Open an issue with the "question" label or start a discussion.

Thank you for contributing to ULC!