# Installation Guide

Universal Language Counter is designed as a **single-file standalone tool** - no installation required!

## Quick Start (Recommended)

```bash
# Download and run immediately
wget https://raw.githubusercontent.com/NeoAxios/ulc/main/ulc.py
python3 ulc.py /path/to/analyze
```

## Installation Options

### Option 1: Direct Download (Simplest)
```bash
# Download ulc.py to your project or ~/bin
curl -O https://raw.githubusercontent.com/NeoAxios/ulc/main/ulc.py
python3 ulc.py .
```

### Option 2: Clone Repository  
```bash
git clone https://github.com/NeoAxios/ulc.git
cd ulc
python3 ulc.py .
```

### Option 3: Add to PATH (System-wide)
```bash
# Download to system location
sudo wget https://raw.githubusercontent.com/NeoAxios/ulc/main/ulc.py -O /usr/local/bin/ulc
sudo chmod +x /usr/local/bin/ulc

# Now use from anywhere
ulc /path/to/project
```

## Enhanced Setup (Optional)

### Install chardet for Better Encoding Detection
```bash
pip install chardet
python3 ulc.py .  # Now handles more file encodings
```

### Install GitHub Linguist for 400+ Languages
```bash
# Requires Ruby
gem install github-linguist
python3 ulc.py . --comprehensive
```

## Requirements

- **Python 3.6+** (standard library only)
- **Optional**: `chardet` for enhanced encoding detection
- **Optional**: `github-linguist` for comprehensive language support

## Verification

Test your installation:
```bash
python3 ulc.py --version
python3 ulc.py --help
python3 ulc.py . --debug
```

## No Installation Needed!

Remember: ULC is designed to work immediately with zero setup. Just download `ulc.py` and run it!