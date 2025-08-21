# Installation Guide

NeoAxios Language Counter is designed as a **single-file standalone tool** - no installation required!

## Quick Start (Recommended)

```bash
# Download and run immediately
wget https://raw.githubusercontent.com/NeoAxios/nxlc/main/nxlc.py
python3 nxlc.py /path/to/analyze
```

## Installation Options

### Option 1: Direct Download (Simplest)
```bash
# Download nxlc.py to your project or ~/bin
curl -O https://raw.githubusercontent.com/NeoAxios/nxlc/main/nxlc.py
python3 nxlc.py .
```

### Option 2: Clone Repository  
```bash
git clone https://github.com/NeoAxios/nxlc.git
cd nxlc
python3 nxlc.py .
```

### Option 3: Add to PATH (System-wide)
```bash
# Download to system location
sudo wget https://raw.githubusercontent.com/NeoAxios/nxlc/main/nxlc.py -O /usr/local/bin/nxlc
sudo chmod +x /usr/local/bin/nxlc

# Now use from anywhere
nxlc /path/to/project
```

## Enhanced Setup (Optional)

### Install chardet for Better Encoding Detection
```bash
pip install chardet
python3 nxlc.py .  # Now handles more file encodings
```

### Install GitHub Linguist for 400+ Languages
```bash
# Requires Ruby
gem install github-linguist
python3 nxlc.py . --comprehensive
```

## Requirements

- **Python 3.6+** (standard library only)
- **Optional**: `chardet` for enhanced encoding detection
- **Optional**: `github-linguist` for comprehensive language support

## Verification

Test your installation:
```bash
python3 nxlc.py --version
python3 nxlc.py --help
python3 nxlc.py . --debug
```

## No Installation Needed!

Remember: NXLC is designed to work immediately with zero setup. Just download `nxlc.py` and run it!