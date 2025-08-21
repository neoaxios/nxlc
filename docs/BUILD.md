# Build and Release Guide

This document explains how to build, test, and release NXLC (NeoAxios Language Counter).

## Development Setup

### Prerequisites
```bash
# Required
python3 -m pip install --upgrade pip setuptools wheel build twine

# Optional (for development)
python3 -m pip install pytest black flake8 chardet
```

### Quick Development Setup
```bash
# Install in development mode
make install-dev

# Or manually:
pip install -e ".[dev]"
```

## Building

### Local Build
```bash
# Build distribution packages
make build

# Or manually:
python3 -m build
```

This creates:
- `dist/nxlc-1.0.0.tar.gz` (source distribution)
- `dist/nxlc-1.0.0-py3-none-any.whl` (wheel)

### Verify Build
```bash
# Check distribution packages
make check-dist

# Test installation from wheel
pip install dist/nxlc-1.0.0-py3-none-any.whl
nxlc --version
```

## Testing

### Run Test Suite
```bash
# Run all tests
make test

# Or manually:
python3 -m pytest tests/ -v
```

### Manual Testing
```bash
# Test basic functionality
make demo

# Test command line interface
python3 nxlc.py --version
python3 nxlc.py --help
python3 nxlc.py . --debug
```

## Publishing

### Test Release (TestPyPI)
```bash
# Upload to TestPyPI first
make upload-test

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ nxlc
nxlc --version
```

### Production Release (PyPI)
```bash
# WARNING: This publishes to production PyPI
make upload

# Or manually with confirmation:
python3 -m twine upload dist/*
```

## Release Checklist

### Pre-Release
- [ ] Update version in `pyproject.toml`
- [ ] Update version in `nxlc.py` (`--version` output)
- [ ] Update `CHANGELOG.md` with new version
- [ ] Run full test suite: `make test`
- [ ] Test build: `make build && make check-dist`
- [ ] Test installation: `pip install dist/*.whl`
- [ ] Update TODO placeholders in `pyproject.toml`:
  - [ ] Author name and email
  - [ ] Homepage URL
  - [ ] Repository URL
  - [ ] Bug tracker URL

### Release Process
- [ ] Tag release: `git tag v1.0.0`
- [ ] Push tags: `git push --tags`
- [ ] Test on TestPyPI: `make upload-test`
- [ ] Verify TestPyPI installation
- [ ] Release to PyPI: `make upload`
- [ ] Create GitHub release with assets
- [ ] Update documentation

### Post-Release
- [ ] Verify PyPI listing: https://pypi.org/project/nxlc/
- [ ] Test installation: `pip install nxlc`
- [ ] Update download counts in README
- [ ] Announce release

## File Structure

```
nxlc/
├── nxlc.py              # Main script (single-file tool)
├── pyproject.toml      # Modern Python packaging
├── setup.cfg           # Setuptools configuration
├── MANIFEST.in         # Package manifest
├── Makefile           # Build automation
├── tests/             # Test suite
│   ├── __init__.py
│   └── test_nxlc.py
├── README.md          # Main documentation
├── INSTALL.md         # Installation guide
├── BUILD.md           # This file
├── CHANGELOG.md       # Version history
├── LICENSE            # MIT license
├── requirements.txt   # Optional dependencies
└── .gitignore        # Git ignore rules
```

## Build Tools

### Required Tools
- `build` - Modern Python build frontend
- `twine` - Secure PyPI uploading
- `setuptools` - Package building backend
- `wheel` - Wheel format support

### Development Tools (Optional)
- `pytest` - Test framework
- `black` - Code formatter
- `flake8` - Linting
- `chardet` - Enhanced encoding detection

## Troubleshooting

### Build Issues
```bash
# Clean and rebuild
make clean
make build

# Check for syntax errors
python3 -c "import ast; ast.parse(open('nxlc.py').read())"

# Test import
python3 -c "import nxlc; print('Import successful')"
```

### Upload Issues
```bash
# Check credentials
python3 -m twine check dist/*

# Upload with verbose output
python3 -m twine upload --verbose dist/*
```

### Testing Issues
```bash
# Run individual test
python3 -m pytest tests/test_nxlc.py::TestNXLC::test_basic -v

# Run with coverage
python3 -m pytest --cov=nxlc tests/
```

## Dual Distribution Strategy

NXLC supports both:

1. **Direct Download**: `wget nxlc.py && python3 nxlc.py`
2. **pip Install**: `pip install nxlc && nxlc`

Both methods use the same `nxlc.py` file, ensuring consistency and simplicity.