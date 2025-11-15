# Changelog

All notable changes to NeoAxios Language Counter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-11-15

### Fixed
- **Critical bug fix**: .gitignore directory patterns now properly respected in git repositories
  - Files in directories like `.testgrid-cache/`, `.build-cache/` are now correctly ignored
  - Root cause: Auto-detection loaded .gitignore patterns but used wrong variable (`use_git` instead of `should_use_git`)
  - Enhanced `is_gitignored()` to use sophisticated pattern matching for directory patterns (trailing `/`)
  - Added directory-level .gitignore checks before recursing into subdirectories

### Added
- Comprehensive test suite for .gitignore functionality (21 new tests + 4 reusable fixtures)
- E2E validation tests for .gitignore directory pattern handling

## [0.1.2] - 2025-08-22

### Changed
- Version bump for PyPI release

## [0.1.0] - 2025-08-18

### Added
- **Hierarchical .nxlcignore support** (now default behavior)
  - Each directory can have its own `.nxlcignore` file
  - Patterns are inherited from parent directories
  - Child patterns add to (don't replace) parent patterns
  - Similar to how `.gitignore` works in git repositories
- **Pattern negation support** (`!pattern` to re-include files)
  - Allows fine-grained control over exclusions
  - Example: `*.log` then `!important.log` keeps important.log
- **Enhanced debug mode** for ignore patterns
  - Shows which `.nxlcignore` file caused a file to be ignored
  - Usage: `nxlc --debug /path/to/project`
- **Thread-safe caching** with LRU eviction strategy
  - Improves performance for large projects
  - Configurable cache size (default 1000 entries)
- **Security enhancements**
  - 1MB file size limit for `.nxlcignore` files
  - Path traversal prevention
  - Input validation for all user inputs

### Changed
- `.nxlcignore` files now work hierarchically by default (no flag needed)
- Improved pattern matching performance with caching
- Better cross-platform path handling

### Fixed
- Python 3.8 compatibility for type annotations
- Pattern matching edge cases with directory patterns

### Technical Improvements
- Clean architecture with Protocol patterns and dependency injection
- Comprehensive test suite (36+ tests for hierarchical functionality)
- Reusable components (CacheStrategy, IgnoreFileReader, PatternMatcher)
- Performance optimizations (often faster than previous flat mode)

## [0.0.1] - 2025-08-15

### Added
- Initial release of NeoAxios Language Counter
- Support for 119+ programming languages
- Smart language conflict resolution for ambiguous extensions
- Git integration with automatic .gitignore respect
- Cross-platform support (Windows, macOS, Linux)
- Thread-safe architecture with instance-based design
- Professional colored terminal output
- Debug mode with unknown file analysis
- Comprehensive error handling and logging
- Security hardening against command injection
- Optional GitHub Linguist integration for 400+ languages
- Configurable output sorting (lines, files, name)
- Verbose and debug modes for troubleshooting

### Language Support
- **Modern Languages**: Python, JavaScript, TypeScript, Vue, Svelte, Java, C, C++, C#, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, Dart, R, Julia
- **Shell & Scripting**: Shell (bash, zsh, fish), PowerShell, Perl, Lua  
- **Data & Config**: SQL, HTML, CSS, Markdown, YAML, JSON, XML, TOML, INI, Properties
- **Legacy Systems**: COBOL, FORTRAN, Pascal, Ada, Assembly, BASIC, Visual Basic
- **Domain-Specific**: VHDL, Verilog, MATLAB, Mathematica, SAS, SPSS, AutoLISP, OpenSCAD
- **And 80+ additional languages**

### Features
- **Smart Detection**: Content analysis for `.h` (C/C++/Objective-C), `.m` (MATLAB/Objective-C), `.r` (R/Rebol), `.pl` (Perl/Prolog)
- **Special Files**: Makefiles, Dockerfiles, READMEs, git config files
- **Shebang Analysis**: Extensionless script detection
- **Performance**: Symlink cycle detection, binary file filtering
- **Security**: Input validation, safe file handling, path traversal protection

### Fixed
- **Critical bug fix**: Python and other languages with symmetric multiline comment delimiters (""", ''') were incorrectly counting all code as comments
- Multiline comment detection now properly handles patterns that both start and end comments
- Python files now show accurate code vs comment line counts

### Technical
- Minimum Python 3.6+ requirement
- Zero mandatory dependencies (chardet optional for enhanced encoding)
- Thread-safe design for concurrent usage
- Comprehensive logging with configurable levels
- Exception handling decorator pattern
- Platform abstraction for cross-platform compatibility
