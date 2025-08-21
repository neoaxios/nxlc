#!/usr/bin/env python3
"""
Fixture Validator for E2E Line Counting Tests

Validates test fixtures for consistency, completeness, and correctness.
Ensures all fixtures meet quality standards before testing.
"""

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
import argparse
import logging
from enum import Enum

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


class ValidationType(Enum):
    """Types of validation checks."""
    STRUCTURE = "structure"
    CONSISTENCY = "consistency"
    COMPLETENESS = "completeness"
    CORRECTNESS = "correctness"
    PERFORMANCE = "performance"


@dataclass
class ValidationIssue:
    """Represents a validation issue found in fixtures."""
    level: ValidationLevel
    type: ValidationType
    path: Path
    message: str
    details: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        """String representation of the issue."""
        return f"[{self.level.value.upper()}] {self.path}: {self.message}"
    
    @property
    def is_error(self) -> bool:
        """Check if this is an error-level issue."""
        return self.level == ValidationLevel.ERROR


@dataclass
class ValidationReport:
    """Complete validation report for fixtures."""
    issues: List[ValidationIssue] = field(default_factory=list)
    stats: Dict[str, int] = field(default_factory=dict)
    
    def add_issue(self, issue: ValidationIssue):
        """Add an issue to the report."""
        self.issues.append(issue)
        
        # Update stats
        level_key = f"{issue.level.value}_count"
        self.stats[level_key] = self.stats.get(level_key, 0) + 1
        
        type_key = f"{issue.type.value}_issues"
        self.stats[type_key] = self.stats.get(type_key, 0) + 1
    
    @property
    def has_errors(self) -> bool:
        """Check if report contains any errors."""
        return any(issue.is_error for issue in self.issues)
    
    @property
    def error_count(self) -> int:
        """Get count of error-level issues."""
        return self.stats.get('error_count', 0)
    
    @property
    def warning_count(self) -> int:
        """Get count of warning-level issues."""
        return self.stats.get('warning_count', 0)
    
    def get_summary(self) -> str:
        """Get summary of validation report."""
        lines = []
        lines.append("=" * 60)
        lines.append("FIXTURE VALIDATION REPORT")
        lines.append("=" * 60)
        
        # Stats
        lines.append(f"\nTotal Issues: {len(self.issues)}")
        lines.append(f"  Errors: {self.error_count}")
        lines.append(f"  Warnings: {self.warning_count}")
        lines.append(f"  Info: {self.stats.get('info_count', 0)}")
        
        # By type
        lines.append("\nBy Type:")
        for vtype in ValidationType:
            count = self.stats.get(f"{vtype.value}_issues", 0)
            if count > 0:
                lines.append(f"  {vtype.value.capitalize()}: {count}")
        
        # Issues
        if self.issues:
            lines.append("\nIssues:")
            
            # Group by level
            for level in [ValidationLevel.ERROR, ValidationLevel.WARNING, ValidationLevel.INFO]:
                level_issues = [i for i in self.issues if i.level == level]
                if level_issues:
                    lines.append(f"\n{level.value.upper()}S:")
                    for issue in level_issues[:10]:  # Show first 10 of each level
                        lines.append(f"  - {issue.path}: {issue.message}")
                    if len(level_issues) > 10:
                        lines.append(f"  ... and {len(level_issues) - 10} more")
        
        lines.append("\n" + "=" * 60)
        
        if self.has_errors:
            lines.append("VALIDATION FAILED - Errors must be fixed")
        else:
            lines.append("VALIDATION PASSED - No critical errors found")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)


class FixtureValidator:
    """Base class for fixture validators."""
    
    def validate(self, path: Path) -> List[ValidationIssue]:
        """Validate a path and return issues found."""
        raise NotImplementedError


class StructureValidator(FixtureValidator):
    """Validates fixture directory structure."""
    
    REQUIRED_CATEGORIES = ['common', 'web', 'systems', 'scripting']
    EXPECTED_FILES = ['simple', 'complex', 'edge_cases']
    
    def validate(self, fixtures_dir: Path) -> List[ValidationIssue]:
        """Validate directory structure."""
        issues = []
        
        # Check fixtures directory exists
        if not fixtures_dir.exists():
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                type=ValidationType.STRUCTURE,
                path=fixtures_dir,
                message="Fixtures directory does not exist"
            ))
            return issues
        
        # Check for required categories
        for category in self.REQUIRED_CATEGORIES:
            category_dir = fixtures_dir / category
            if not category_dir.exists():
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    type=ValidationType.STRUCTURE,
                    path=category_dir,
                    message=f"Required category '{category}' is missing"
                ))
        
        # Check each category
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            # Check for at least one language
            language_dirs = [d for d in category_dir.iterdir() if d.is_dir()]
            if not language_dirs:
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    type=ValidationType.STRUCTURE,
                    path=category_dir,
                    message="Category has no language directories"
                ))
            
            # Check each language directory
            for lang_dir in language_dirs:
                issues.extend(self._validate_language_dir(lang_dir))
        
        return issues
    
    def _validate_language_dir(self, lang_dir: Path) -> List[ValidationIssue]:
        """Validate a language directory structure."""
        issues = []
        
        # Check for expected.json
        expected_file = lang_dir / "expected.json"
        if not expected_file.exists():
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                type=ValidationType.STRUCTURE,
                path=lang_dir,
                message="Missing expected.json file"
            ))
            return issues  # Can't validate further without expected.json
        
        # Load expected.json
        try:
            with open(expected_file, 'r') as f:
                expected_data = json.load(f)
        except json.JSONDecodeError as e:
            issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                type=ValidationType.STRUCTURE,
                path=expected_file,
                message=f"Invalid JSON: {e}"
            ))
            return issues
        
        # Check for fixture files
        for fixture_type in self.EXPECTED_FILES:
            if fixture_type not in expected_data:
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    type=ValidationType.STRUCTURE,
                    path=lang_dir,
                    message=f"Missing fixture type '{fixture_type}' in expected.json"
                ))
                continue
            
            fixture_info = expected_data[fixture_type]
            fixture_file = lang_dir / fixture_info.get('filename', f'{fixture_type}.txt')
            
            if not fixture_file.exists():
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    type=ValidationType.STRUCTURE,
                    path=fixture_file,
                    message=f"Fixture file does not exist"
                ))
        
        return issues


class ConsistencyValidator(FixtureValidator):
    """Validates consistency within and across fixtures."""
    
    def validate(self, fixtures_dir: Path) -> List[ValidationIssue]:
        """Validate consistency."""
        issues = []
        
        # Collect all languages and their data
        language_data = {}
        
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            for lang_dir in category_dir.iterdir():
                if not lang_dir.is_dir():
                    continue
                
                expected_file = lang_dir / "expected.json"
                if expected_file.exists():
                    try:
                        with open(expected_file, 'r') as f:
                            data = json.load(f)
                            language = data.get('language', lang_dir.name)
                            
                            if language in language_data:
                                # Duplicate language found
                                issues.append(ValidationIssue(
                                    level=ValidationLevel.ERROR,
                                    type=ValidationType.CONSISTENCY,
                                    path=lang_dir,
                                    message=f"Duplicate language '{language}' found",
                                    details={
                                        'first_occurrence': str(language_data[language]['path']),
                                        'duplicate': str(lang_dir)
                                    }
                                ))
                            else:
                                language_data[language] = {
                                    'path': lang_dir,
                                    'data': data,
                                    'category': category_dir.name
                                }
                    except Exception as e:
                        # Skip files with errors (handled by structure validator)
                        pass
        
        # Check consistency within each language
        for language, info in language_data.items():
            issues.extend(self._validate_language_consistency(
                language, info['path'], info['data']
            ))
        
        return issues
    
    def _validate_language_consistency(self, 
                                      language: str,
                                      path: Path,
                                      data: Dict) -> List[ValidationIssue]:
        """Validate consistency within a language's fixtures."""
        issues = []
        
        # Check required fields in expected.json
        required_fields = ['language', 'category']
        for field in required_fields:
            if field not in data:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    type=ValidationType.CONSISTENCY,
                    path=path / "expected.json",
                    message=f"Missing required field '{field}'"
                ))
        
        # Check count fields for each fixture type
        for fixture_type in ['simple', 'complex', 'edge_cases']:
            if fixture_type not in data:
                continue
            
            fixture_data = data[fixture_type]
            required_counts = ['total', 'code', 'comments', 'blank']
            
            for count_field in required_counts:
                if count_field not in fixture_data:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        type=ValidationType.CONSISTENCY,
                        path=path / "expected.json",
                        message=f"Missing count field '{count_field}' in {fixture_type}"
                    ))
                elif not isinstance(fixture_data[count_field], int):
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        type=ValidationType.CONSISTENCY,
                        path=path / "expected.json",
                        message=f"Count field '{count_field}' in {fixture_type} must be an integer"
                    ))
        
        return issues


class CompletenessValidator(FixtureValidator):
    """Validates completeness of test coverage."""
    
    MIN_LANGUAGES_PER_CATEGORY = 3
    
    def validate(self, fixtures_dir: Path) -> List[ValidationIssue]:
        """Validate completeness."""
        issues = []
        
        # Count languages per category
        category_counts = {}
        
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            language_count = 0
            for lang_dir in category_dir.iterdir():
                if lang_dir.is_dir() and (lang_dir / "expected.json").exists():
                    language_count += 1
            
            category_counts[category_dir.name] = language_count
            
            if language_count < self.MIN_LANGUAGES_PER_CATEGORY:
                issues.append(ValidationIssue(
                    level=ValidationLevel.INFO,
                    type=ValidationType.COMPLETENESS,
                    path=category_dir,
                    message=f"Category has only {language_count} languages (minimum recommended: {self.MIN_LANGUAGES_PER_CATEGORY})"
                ))
        
        # Check overall coverage
        total_languages = sum(category_counts.values())
        if total_languages < 10:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                type=ValidationType.COMPLETENESS,
                path=fixtures_dir,
                message=f"Only {total_languages} languages available for testing"
            ))
        
        return issues


class CorrectnessValidator(FixtureValidator):
    """Validates correctness of line counts."""
    
    def validate(self, fixtures_dir: Path) -> List[ValidationIssue]:
        """Validate correctness."""
        issues = []
        
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            for lang_dir in category_dir.iterdir():
                if not lang_dir.is_dir():
                    continue
                
                issues.extend(self._validate_language_correctness(lang_dir))
        
        return issues
    
    def _validate_language_correctness(self, lang_dir: Path) -> List[ValidationIssue]:
        """Validate correctness of counts for a language."""
        issues = []
        
        expected_file = lang_dir / "expected.json"
        if not expected_file.exists():
            return issues
        
        try:
            with open(expected_file, 'r') as f:
                expected_data = json.load(f)
        except:
            return issues
        
        # Validate each fixture
        for fixture_type in ['simple', 'complex', 'edge_cases']:
            if fixture_type not in expected_data:
                continue
            
            fixture_info = expected_data[fixture_type]
            fixture_file = lang_dir / fixture_info.get('filename', f'{fixture_type}.txt')
            
            if not fixture_file.exists():
                continue
            
            # Read actual file
            try:
                with open(fixture_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            except Exception as e:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    type=ValidationType.CORRECTNESS,
                    path=fixture_file,
                    message=f"Cannot read file: {e}"
                ))
                continue
            
            # Basic validation
            actual_total = len(lines)
            expected_total = fixture_info.get('total', 0)
            
            if actual_total != expected_total:
                issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    type=ValidationType.CORRECTNESS,
                    path=fixture_file,
                    message=f"Line count mismatch: file has {actual_total} lines, expected {expected_total}"
                ))
            
            # Validate sum of counts
            code = fixture_info.get('code', 0)
            comments = fixture_info.get('comments', 0)
            blank = fixture_info.get('blank', 0)
            
            # Note: code + comments + blank may not equal total
            # because lines can be counted as both code and comment (mixed lines)
            # But the sum should not exceed total
            if code + blank > expected_total:
                issues.append(ValidationIssue(
                    level=ValidationLevel.WARNING,
                    type=ValidationType.CORRECTNESS,
                    path=fixture_file,
                    message=f"Count sum issue: code({code}) + blank({blank}) > total({expected_total})"
                ))
            
            # Check for negative counts
            for count_name, count_value in [('code', code), ('comments', comments), ('blank', blank)]:
                if count_value < 0:
                    issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        type=ValidationType.CORRECTNESS,
                        path=fixture_file,
                        message=f"Negative count for {count_name}: {count_value}"
                    ))
        
        return issues


class PerformanceValidator(FixtureValidator):
    """Validates performance characteristics of fixtures."""
    
    MAX_FILE_SIZE = 100 * 1024  # 100KB
    MAX_LINE_LENGTH = 1000
    
    def validate(self, fixtures_dir: Path) -> List[ValidationIssue]:
        """Validate performance characteristics."""
        issues = []
        
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            for lang_dir in category_dir.iterdir():
                if not lang_dir.is_dir():
                    continue
                
                # Check each fixture file
                for file_path in lang_dir.iterdir():
                    if file_path.suffix == '.json':
                        continue  # Skip JSON files
                    
                    if file_path.is_file():
                        issues.extend(self._validate_file_performance(file_path))
        
        return issues
    
    def _validate_file_performance(self, file_path: Path) -> List[ValidationIssue]:
        """Validate performance characteristics of a file."""
        issues = []
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                type=ValidationType.PERFORMANCE,
                path=file_path,
                message=f"File size ({file_size} bytes) exceeds recommended maximum ({self.MAX_FILE_SIZE} bytes)"
            ))
        
        # Check line lengths
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for i, line in enumerate(f, 1):
                    if len(line) > self.MAX_LINE_LENGTH:
                        issues.append(ValidationIssue(
                            level=ValidationLevel.INFO,
                            type=ValidationType.PERFORMANCE,
                            path=file_path,
                            message=f"Line {i} exceeds {self.MAX_LINE_LENGTH} characters",
                            details={'line_number': i, 'length': len(line)}
                        ))
                        break  # Only report first occurrence
        except Exception:
            # Ignore read errors (handled by other validators)
            pass
        
        return issues


class FixtureValidatorSuite:
    """Suite of all validators."""
    
    def __init__(self):
        """Initialize validator suite."""
        self.validators = [
            StructureValidator(),
            ConsistencyValidator(),
            CompletenessValidator(),
            CorrectnessValidator(),
            PerformanceValidator()
        ]
    
    def validate(self, fixtures_dir: Path) -> ValidationReport:
        """Run all validators and generate report."""
        report = ValidationReport()
        
        for validator in self.validators:
            logger.info(f"Running {validator.__class__.__name__}...")
            issues = validator.validate(fixtures_dir)
            
            for issue in issues:
                report.add_issue(issue)
        
        return report
    
    def validate_specific(self, 
                         fixtures_dir: Path,
                         validators: List[str]) -> ValidationReport:
        """Run specific validators."""
        report = ValidationReport()
        
        validator_map = {v.__class__.__name__.lower(): v for v in self.validators}
        
        for validator_name in validators:
            validator = validator_map.get(validator_name.lower())
            if validator:
                logger.info(f"Running {validator.__class__.__name__}...")
                issues = validator.validate(fixtures_dir)
                
                for issue in issues:
                    report.add_issue(issue)
            else:
                logger.warning(f"Unknown validator: {validator_name}")
        
        return report


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Validate E2E test fixtures')
    parser.add_argument('--fixtures', '-f', type=Path,
                       default=Path(__file__).parent / 'fixtures',
                       help='Path to fixtures directory')
    parser.add_argument('--validator', '-v', action='append',
                       help='Run specific validator(s)')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output path for validation report')
    parser.add_argument('--json', action='store_true',
                       help='Output report as JSON')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Only show errors')
    parser.add_argument('--strict', action='store_true',
                       help='Treat warnings as errors')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.ERROR)
    
    # Create validator suite
    suite = FixtureValidatorSuite()
    
    # Run validation
    if args.validator:
        report = suite.validate_specific(args.fixtures, args.validator)
    else:
        report = suite.validate(args.fixtures)
    
    # Handle strict mode
    if args.strict and report.warning_count > 0:
        # Convert warnings to errors
        for issue in report.issues:
            if issue.level == ValidationLevel.WARNING:
                issue.level = ValidationLevel.ERROR
        report.stats['error_count'] = report.stats.get('error_count', 0) + report.warning_count
        report.stats['warning_count'] = 0
    
    # Output report
    if args.json:
        output = {
            'stats': report.stats,
            'issues': [
                {
                    'level': issue.level.value,
                    'type': issue.type.value,
                    'path': str(issue.path),
                    'message': issue.message,
                    'details': issue.details
                }
                for issue in report.issues
            ]
        }
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(output, f, indent=2)
        else:
            print(json.dumps(output, indent=2))
    else:
        summary = report.get_summary()
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(summary)
        else:
            print(summary)
    
    # Return appropriate exit code
    return 1 if report.has_errors else 0


if __name__ == '__main__':
    sys.exit(main())