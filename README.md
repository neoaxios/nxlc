# Universal Language Counter (ULC)

A fast, comprehensive programming language line counter supporting 119+ languages with intelligent conflict resolution and git integration.

## Features

- **119+ Programming Languages**: From modern languages (Python, JavaScript, Rust) to legacy (COBOL, FORTRAN) and domain-specific (VHDL, MATLAB)
- **Smart Language Detection**: Content analysis for ambiguous extensions (`.h`, `.m`, `.r`, `.pl`)
- **Git Integration**: Auto-detects git repositories and respects `.gitignore` patterns
- **Custom Ignore Files**: Support for `.ulcignore` to exclude files/directories from counting
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Colored Output**: Professional terminal output with color coding
- **Debug Mode**: Unknown file analysis and extension reporting
- **Security-First**: Input validation and safe file handling

## Quick Start

```bash
# Count current directory
python3 ulc.py

# Count specific project with git integration
python3 ulc.py /path/to/project

# Debug mode to see unknown files
python3 ulc.py . --debug

# Sort by file count, no colors
python3 ulc.py . --sort files --no-color
```

## Installation

ULC is a **single-file standalone tool** - no installation required!

```bash
# Download and run immediately  
wget https://raw.githubusercontent.com/your-org/ulc/main/ulc.py
python3 ulc.py /path/to/analyze
```

### Optional Enhancements
```bash
# Better encoding detection (recommended)
pip install chardet

# 400+ language support (requires Ruby)
gem install github-linguist
python3 ulc.py --comprehensive
```

See [INSTALL.md](docs/INSTALL.md) for detailed installation options.

## Usage

```
usage: ulc.py [-h] [--git] [--no-git] [--depth N] [--sort {lines,files,name}]
              [--verbose] [--comprehensive] [--linguist-path PATH]
              [--no-color] [--debug] [--version]
              [directory]

Universal Language Counter - Count lines of code across 119+ programming languages

positional arguments:
  directory             Directory to analyze (default: current directory)

options:
  -h, --help            show this help message and exit
  --git                 Force respect .gitignore patterns (auto-detected in git repos)
  --no-git              Disable git integration (ignore .gitignore even in git repos)
  --depth N             Maximum directory depth to traverse
  --sort {lines,files,name}
                        Sort results by lines (default), files, or name
  --verbose, -v         Verbose output showing each file processed
  --comprehensive       Use comprehensive mode with GitHub Linguist (400+ languages)
  --linguist-path PATH  Path to github-linguist executable
  --no-color            Disable colored output
  --debug               Enable debug mode (show unknown files and extension analysis)
  --version             show program's version number and exit
```

## Examples

### Basic Usage
```bash
# Count lines in current directory
python3 ulc.py

# Count specific directory
python3 ulc.py /path/to/project

# Limit directory traversal depth
python3 ulc.py . --depth 3
```

### Git Integration
```bash
# Auto-detects git repos and respects .gitignore
python3 ulc.py /path/to/git/repo

# Force git mode even outside repos
python3 ulc.py . --git

# Disable git integration completely
python3 ulc.py . --no-git
```

### Ignore Files with .ulcignore
ULC supports a `.ulcignore` file to exclude specific files and directories from counting. This works independently of git and is useful for:
- Non-git repositories
- Additional exclusions beyond .gitignore
- Temporary exclusions during development

Create a `.ulcignore` file in your project root:
```bash
# Example .ulcignore
node_modules/
dist/
*.min.js
test_data/
*.generated.*
```

See `.ulcignore.example` for a comprehensive template.

### Output Customization
```bash
# Sort by file count instead of lines
python3 ulc.py . --sort files

# Sort alphabetically by language
python3 ulc.py . --sort name

# Disable colored output for scripts
python3 ulc.py . --no-color

# Verbose mode shows each file processed
python3 ulc.py . --verbose
```

### Advanced Features
```bash
# Debug mode shows unknown file extensions
python3 ulc.py . --debug

# Comprehensive mode with GitHub Linguist
python3 ulc.py . --comprehensive

# Custom linguist path
python3 ulc.py . --comprehensive --linguist-path /custom/path/linguist
```

## Platform Compatibility

| Platform | Environment                | 119+ Native Languages | GitHub Linguist (400+) | Status       |
|----------|----------------------------|-----------------------|------------------------|--------------|
| Linux    | WSL2 (Ubuntu 24.04)        | ✅ Validated          | 🔄 Not tested          | ✅ Validated |
| Linux    | Native Ubuntu 22.04+       | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Linux    | RHEL/CentOS 8+             | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Linux    | Debian 11+                 | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| macOS    | macOS 12+ (Intel)          | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| macOS    | macOS 14+ (Apple Silicon)  | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Windows  | Windows 10/11 (native)     | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Windows  | Git Bash                   | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Windows  | PowerShell 7               | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Docker   | Alpine Linux               | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Docker   | Ubuntu based               | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Cloud    | GitHub Codespaces          | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| Cloud    | GitLab CI/CD               | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |
| BSD      | FreeBSD 13+                | 🔄 Not tested         | 🔄 Not tested          | 🔄 Pending   |

**Notes:**
- **Native language support**: 119+ languages without external dependencies
- **GitHub Linguist integration**: Optional, adds 400+ languages (requires Ruby)
- **Python requirement**: 3.8+ (tested with 3.12)

## Supported Languages

### Modern Languages (Web, Mobile, Systems)
Python, JavaScript, TypeScript, Vue, Svelte, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, Dart, R, Julia

### Shell & Scripting  
Shell (bash, zsh, fish), PowerShell, Perl, Lua

### Data & Config
SQL, HTML, CSS, Markdown, YAML, JSON, XML, TOML, INI, Properties

### Legacy Systems
COBOL, FORTRAN, Pascal, Ada, Assembly, BASIC, Visual Basic

### Domain-Specific
VHDL, Verilog, MATLAB, Mathematica, SAS, SPSS, AutoLISP, OpenSCAD

### And 80+ more languages...

## Sample Output

```
Universal Language Counter Results:
--------------------------------------------------------------------------------
Language             Files    Total      Code       Comments   %     
--------------------------------------------------------------------------------
Total                156      45,234     38,891     4,829      100.0%
--------------------------------------------------------------------------------
Python               89       28,456     25,123     2,891      62.9 %
JavaScript           23       8,234      7,456      623        18.2 %
Markdown             18       4,891      4,201      0          10.8 %
JSON                 12       2,134      2,134      0          4.7  %
Shell                8        891        634        89         2.0  %
YAML                 6        628        567        226        1.4  %
--------------------------------------------------------------------------------
Directory: /path/to/project (git repository - respecting .gitignore)
```

## Language Detection Features

### Smart Conflict Resolution
- **`.h` files**: Distinguishes C, C++, and Objective-C by content analysis
- **`.m` files**: Separates MATLAB from Objective-C based on syntax patterns  
- **`.r` files**: Identifies R vs Rebol using language-specific keywords
- **`.pl` files**: Differentiates Perl from Prolog through code analysis

### Special File Handling
- **Makefiles**: Recognizes various Makefile variants
- **Dockerfiles**: Detects Dockerfile patterns
- **READMEs**: Identifies documentation files
- **Git config**: Classifies `.gitignore`, `.gitattributes` as configuration
- **Shebang detection**: Analyzes `#!/usr/bin/env` headers for extensionless scripts

## Architecture

### Thread-Safe Design
- Instance-based color management
- Thread-safe linguist integration
- Concurrent-safe file processing

### Security Features
- Input validation for external tool paths
- Command injection prevention  
- Safe file encoding detection
- Path traversal protection

### Performance Optimizations
- Symlink cycle detection
- Binary file filtering
- Efficient directory traversal
- Configurable depth limits

## Requirements

- **Python 3.6+** (required)
- **chardet** (optional, recommended for encoding detection)
- **github-linguist** (optional, for 400+ language support)

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT License - see LICENSE file for details.

## Version History

- **v1.0.0** - Initial release with 119+ language support
  - Smart conflict resolution
  - Git integration  
  - Cross-platform support
  - Thread-safe architecture
  - Security hardening

---

**Universal Language Counter** - Professional code analysis made simple.