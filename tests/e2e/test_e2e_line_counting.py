#!/usr/bin/env python3
"""
E2E Line Counting Test Suite

A comprehensive end-to-end testing framework for validating line counting
accuracy across 400+ programming languages. Designed for maintainability,
extensibility, and performance.
"""

import json
import os
import sys
import time
import unittest
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple, Union
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import platform

# Import fixture utilities for centralized configuration
sys.path.insert(0, str(Path(__file__).parent))
from fixture_utils import config

# Use config for consistent paths
PROJECT_ROOT = config.project_root
sys.path.insert(0, str(PROJECT_ROOT / 'src'))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Priority(Enum):
    """Test priority levels for organizing test execution."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Status(Enum):
    """Test execution status."""
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"
    SKIPPED = "skipped"
    ERROR = "error"


@dataclass
class LineCount:
    """Represents line count data for a file."""
    total: int
    code: int
    comments: int
    blank: int
    
    def matches(self, other: 'LineCount', tolerance: float = 0.0) -> bool:
        """Check if counts match within tolerance."""
        if tolerance == 0.0:
            return (self.total == other.total and
                    self.code == other.code and
                    self.comments == other.comments and
                    self.blank == other.blank)
        else:
            # Allow for percentage-based tolerance
            def within_tolerance(a: int, b: int) -> bool:
                if a == 0 and b == 0:
                    return True
                max_val = max(a, b)
                if max_val == 0:
                    return True
                return abs(a - b) / max_val <= tolerance
            
            return (within_tolerance(self.total, other.total) and
                    within_tolerance(self.code, other.code) and
                    within_tolerance(self.comments, other.comments) and
                    within_tolerance(self.blank, other.blank))
    
    def to_dict(self) -> Dict[str, int]:
        """Convert to dictionary representation."""
        return {
            'total': self.total,
            'code': self.code,
            'comments': self.comments,
            'blank': self.blank
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, int]) -> 'LineCount':
        """Create from dictionary representation."""
        return cls(
            total=data['total'],
            code=data['code'],
            comments=data['comments'],
            blank=data['blank']
        )


@dataclass
class Fixture:
    """Represents a test fixture for a language."""
    language: str
    category: str
    file_path: Path
    expected_count: LineCount
    fixture_type: str  # 'simple', 'complex', 'edge_cases'
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def relative_path(self) -> Path:
        """Get path relative to fixtures directory."""
        fixtures_dir = Path(__file__).parent / 'fixtures'
        return self.file_path.relative_to(fixtures_dir)
    
    def validate(self) -> Tuple[bool, Optional[str]]:
        """Validate fixture file exists and is readable."""
        if not self.file_path.exists():
            return False, f"File does not exist: {self.file_path}"
        
        if not self.file_path.is_file():
            return False, f"Not a file: {self.file_path}"
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                f.read(1)  # Try reading first byte
            return True, None
        except Exception as e:
            return False, f"Cannot read file: {e}"


@dataclass
class Result:
    """Represents the result of a single test execution."""
    fixture: Fixture
    actual_count: Optional[LineCount]
    status: Status
    error_message: Optional[str] = None
    execution_time: float = 0.0
    platform_info: Dict[str, str] = field(default_factory=dict)
    
    @property
    def passed(self) -> bool:
        """Check if test passed."""
        return self.status == Status.PASSED
    
    @property
    def failed(self) -> bool:
        """Check if test failed."""
        return self.status == Status.FAILED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'language': self.fixture.language,
            'category': self.fixture.category,
            'fixture_type': self.fixture.fixture_type,
            'file': str(self.fixture.relative_path),
            'status': self.status.value,
            'expected': self.fixture.expected_count.to_dict(),
            'actual': self.actual_count.to_dict() if self.actual_count else None,
            'error': self.error_message,
            'execution_time': self.execution_time,
            'platform': self.platform_info
        }


class LanguageTestStrategy(ABC):
    """Abstract base class for language-specific test strategies."""
    
    @abstractmethod
    def prepare_fixture(self, fixture: Fixture) -> Fixture:
        """Prepare fixture for testing (language-specific setup)."""
        pass
    
    @abstractmethod
    def validate_result(self, fixture: Fixture, result: Result) -> Result:
        """Validate test result with language-specific rules."""
        pass
    
    @abstractmethod
    def get_tolerance(self) -> float:
        """Get acceptable tolerance for count differences."""
        pass


class DefaultTestStrategy(LanguageTestStrategy):
    """Default test strategy for most languages."""
    
    def prepare_fixture(self, fixture: Fixture) -> Fixture:
        """Default preparation (no-op)."""
        return fixture
    
    def validate_result(self, fixture: Fixture, result: Result) -> Result:
        """Default validation."""
        return result
    
    def get_tolerance(self) -> float:
        """Default tolerance is 0 (exact match required)."""
        return 0.0


class TestStrategyFactory:
    """Factory for creating language-specific test strategies."""
    
    _strategies: Dict[str, LanguageTestStrategy] = {}
    
    @classmethod
    def register_strategy(cls, language: str, strategy: LanguageTestStrategy):
        """Register a custom strategy for a language."""
        cls._strategies[language.lower()] = strategy
    
    @classmethod
    def get_strategy(cls, language: str) -> LanguageTestStrategy:
        """Get strategy for a language (returns default if not found)."""
        return cls._strategies.get(language.lower(), DefaultTestStrategy())


class LineCounterInterface(ABC):
    """Interface for line counting implementations."""
    
    @abstractmethod
    def count_lines(self, file_path: Path) -> LineCount:
        """Count lines in a file."""
        pass


class NXLCLineCounter(LineCounterInterface):
    """Line counter using the NXLC tool."""
    
    def __init__(self, nxlc_path: Optional[Path] = None):
        """Initialize with optional custom NXLC path."""
        if nxlc_path:
            self.nxlc_path = nxlc_path
        else:
            # Use the local development version
            self.nxlc_path = PROJECT_ROOT / 'src' / 'nxlc.py'
        
        if not self.nxlc_path.exists():
            raise FileNotFoundError(f"NXLC not found at {self.nxlc_path}")
    
    def count_lines(self, file_path: Path) -> LineCount:
        """Count lines using NXLC."""
        try:
            # Create a temporary directory with just this file to analyze
            import tempfile
            import shutil
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Copy file to temp directory to analyze it in isolation
                tmp_file = Path(tmpdir) / file_path.name
                shutil.copy2(file_path, tmp_file)
                
                # Run NXLC on the temp directory
                result = subprocess.run(
                    [sys.executable, str(self.nxlc_path), tmpdir, '--no-git', '--no-color'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    raise RuntimeError(f"NXLC failed: {result.stderr}")
                
                # Parse text output
                return self._parse_nxlc_output(result.stdout, file_path.name)
            
        except subprocess.TimeoutExpired:
            raise RuntimeError("NXLC execution timed out")
        except Exception as e:
            raise RuntimeError(f"Error running NXLC: {e}")
    
    def _parse_nxlc_output(self, output: str, filename: str) -> LineCount:
        """Parse NXLC text output to extract line counts."""
        lines = output.strip().split('\n')
        
        # Look for the data line (not the Total line)
        # The format is: Language  Files  Total  Code  Comments  %
        in_table = False
        
        for line in lines:
            # Skip empty lines and separator lines
            if not line.strip() or '-' * 10 in line:
                continue
            
            # Check for header
            if 'Language' in line and 'Files' in line and 'Total' in line:
                in_table = True
                continue
            
            # If we're in the table and past the header
            if in_table:
                # Skip the total line
                if line.strip().startswith('Total'):
                    continue
                
                # Parse data line - split by whitespace since no pipes in output
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        # Extract counts (format: Language Files Total Code Comments %)
                        # Skip language name (parts[0]) and files count (parts[1])
                        total_lines = int(parts[2])
                        code_count = int(parts[3])
                        comment_count = int(parts[4])
                        # Calculate blank lines
                        blank_count = total_lines - code_count - comment_count
                        
                        return LineCount(
                            total=total_lines,
                            code=code_count,
                            comments=comment_count,
                            blank=blank_count
                        )
                    except (ValueError, IndexError):
                        continue
        
        # If we couldn't parse the output, raise an error
        raise ValueError(f"Could not parse NXLC output for {filename}")


class Executor:
    """Executes tests with various strategies and configurations."""
    
    def __init__(self, 
                 line_counter: LineCounterInterface,
                 parallel: bool = True,
                 max_workers: int = 4):
        """Initialize test executor."""
        self.line_counter = line_counter
        self.parallel = parallel
        self.max_workers = max_workers
        self.platform_info = self._get_platform_info()
    
    def _get_platform_info(self) -> Dict[str, str]:
        """Get platform information for test results."""
        return {
            'platform': platform.system(),
            'platform_release': platform.release(),
            'platform_version': platform.version(),
            'python_version': platform.python_version(),
            'processor': platform.processor()
        }
    
    def execute_fixture(self, fixture: Fixture) -> Result:
        """Execute a single test fixture."""
        start_time = time.time()
        
        try:
            # Validate fixture
            valid, error = fixture.validate()
            if not valid:
                return Result(
                    fixture=fixture,
                    actual_count=None,
                    status=Status.ERROR,
                    error_message=error,
                    execution_time=time.time() - start_time,
                    platform_info=self.platform_info
                )
            
            # Get test strategy
            strategy = TestStrategyFactory.get_strategy(fixture.language)
            
            # Prepare fixture
            prepared_fixture = strategy.prepare_fixture(fixture)
            
            # Count lines
            actual_count = self.line_counter.count_lines(prepared_fixture.file_path)
            
            # Check if counts match
            tolerance = strategy.get_tolerance()
            if fixture.expected_count.matches(actual_count, tolerance):
                status = Status.PASSED
                error_message = None
            else:
                status = Status.FAILED
                error_message = (
                    f"Count mismatch - "
                    f"Expected: {fixture.expected_count.to_dict()}, "
                    f"Actual: {actual_count.to_dict()}"
                )
            
            # Create result
            result = Result(
                fixture=prepared_fixture,
                actual_count=actual_count,
                status=status,
                error_message=error_message,
                execution_time=time.time() - start_time,
                platform_info=self.platform_info
            )
            
            # Validate result
            return strategy.validate_result(prepared_fixture, result)
            
        except Exception as e:
            return Result(
                fixture=fixture,
                actual_count=None,
                status=Status.ERROR,
                error_message=str(e),
                execution_time=time.time() - start_time,
                platform_info=self.platform_info
            )
    
    def execute_fixtures(self, 
                        fixtures: List[Fixture],
                        progress_callback: Optional[callable] = None) -> List[Result]:
        """Execute multiple test fixtures."""
        results = []
        
        if self.parallel and len(fixtures) > 1:
            # Parallel execution
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_fixture = {
                    executor.submit(self.execute_fixture, fixture): fixture
                    for fixture in fixtures
                }
                
                for future in as_completed(future_to_fixture):
                    result = future.result()
                    results.append(result)
                    
                    if progress_callback:
                        progress_callback(result, len(results), len(fixtures))
        else:
            # Sequential execution
            for i, fixture in enumerate(fixtures, 1):
                result = self.execute_fixture(fixture)
                results.append(result)
                
                if progress_callback:
                    progress_callback(result, i, len(fixtures))
        
        return results


class TestReporter:
    """Generates test reports in various formats."""
    
    @staticmethod
    def generate_summary(results: List[Result]) -> Dict[str, Any]:
        """Generate summary statistics from test results."""
        total = len(results)
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if r.failed)
        errors = sum(1 for r in results if r.status == Status.ERROR)
        skipped = sum(1 for r in results if r.status == Status.SKIPPED)
        
        # Group by category
        by_category = {}
        for result in results:
            category = result.fixture.category
            if category not in by_category:
                by_category[category] = {
                    'total': 0, 'passed': 0, 'failed': 0, 'errors': 0
                }
            by_category[category]['total'] += 1
            if result.passed:
                by_category[category]['passed'] += 1
            elif result.failed:
                by_category[category]['failed'] += 1
            elif result.status == Status.ERROR:
                by_category[category]['errors'] += 1
        
        # Calculate execution time stats
        execution_times = [r.execution_time for r in results]
        avg_time = sum(execution_times) / len(execution_times) if execution_times else 0
        
        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'errors': errors,
            'skipped': skipped,
            'pass_rate': (passed / total * 100) if total > 0 else 0,
            'by_category': by_category,
            'total_execution_time': sum(execution_times),
            'average_execution_time': avg_time,
            'fastest': min(execution_times) if execution_times else 0,
            'slowest': max(execution_times) if execution_times else 0
        }
    
    @staticmethod
    def generate_detailed_report(results: List[Result]) -> str:
        """Generate detailed text report."""
        lines = []
        lines.append("=" * 80)
        lines.append("E2E LINE COUNTING TEST REPORT")
        lines.append("=" * 80)
        
        # Summary
        summary = TestReporter.generate_summary(results)
        lines.append(f"\nSummary:")
        lines.append(f"  Total Tests: {summary['total']}")
        lines.append(f"  Passed: {summary['passed']} ({summary['pass_rate']:.1f}%)")
        lines.append(f"  Failed: {summary['failed']}")
        lines.append(f"  Errors: {summary['errors']}")
        lines.append(f"  Skipped: {summary['skipped']}")
        lines.append(f"  Total Time: {summary['total_execution_time']:.2f}s")
        lines.append(f"  Average Time: {summary['average_execution_time']:.3f}s")
        
        # By category
        lines.append(f"\nBy Category:")
        for category, stats in summary['by_category'].items():
            lines.append(f"  {category}:")
            lines.append(f"    Total: {stats['total']}")
            lines.append(f"    Passed: {stats['passed']}")
            lines.append(f"    Failed: {stats['failed']}")
            lines.append(f"    Errors: {stats['errors']}")
        
        # Failed tests
        failed_tests = [r for r in results if r.failed or r.status == Status.ERROR]
        if failed_tests:
            lines.append(f"\nFailed Tests ({len(failed_tests)}):")
            for result in failed_tests:
                lines.append(f"\n  {result.fixture.language} - {result.fixture.fixture_type}")
                lines.append(f"    File: {result.fixture.relative_path}")
                lines.append(f"    Status: {result.status.value}")
                lines.append(f"    Error: {result.error_message}")
                if result.actual_count:
                    lines.append(f"    Expected: {result.fixture.expected_count.to_dict()}")
                    lines.append(f"    Actual: {result.actual_count.to_dict()}")
        
        lines.append("\n" + "=" * 80)
        return "\n".join(lines)
    
    @staticmethod
    def save_json_report(results: List[Result], output_path: Path):
        """Save test results as JSON."""
        report = {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'summary': TestReporter.generate_summary(results),
            'results': [r.to_dict() for r in results]
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)


class TestE2ELineCounting(unittest.TestCase):
    """Main test class for E2E line counting tests."""
    
    @classmethod
    def setUpClass(cls):
        """Set up test class."""
        cls.fixtures_dir = Path(__file__).parent / 'fixtures'
        cls.line_counter = NXLCLineCounter()
        cls.executor = Executor(cls.line_counter)
        cls.results = []
    
    def setUp(self):
        """Set up individual test."""
        self.start_time = time.time()
    
    def tearDown(self):
        """Tear down individual test."""
        elapsed = time.time() - self.start_time
        logger.debug(f"Test took {elapsed:.3f}s")
    
    @classmethod
    def load_fixtures_for_language(cls, language_dir: Path) -> List[Fixture]:
        """Load all fixtures for a language."""
        fixtures = []
        
        # Load expected.json
        expected_file = language_dir / 'expected.json'
        if not expected_file.exists():
            logger.warning(f"No expected.json found in {language_dir}")
            return fixtures
        
        try:
            with open(expected_file, 'r') as f:
                expected_data = json.load(f)
        except Exception as e:
            logger.error(f"Failed to load {expected_file}: {e}")
            return fixtures
        
        language = expected_data.get('language', language_dir.name)
        category = language_dir.parent.name
        
        # Load fixtures for each type
        for fixture_type in ['simple', 'complex', 'edge_cases']:
            if fixture_type not in expected_data:
                continue
            
            fixture_info = expected_data[fixture_type]
            file_path = language_dir / fixture_info['filename']
            
            if not file_path.exists():
                logger.warning(f"Fixture file not found: {file_path}")
                continue
            
            fixture = Fixture(
                language=language,
                category=category,
                file_path=file_path,
                expected_count=LineCount.from_dict({
                    'total': fixture_info['total'],
                    'code': fixture_info['code'],
                    'comments': fixture_info['comments'],
                    'blank': fixture_info['blank']
                }),
                fixture_type=fixture_type,
                metadata=fixture_info.get('metadata', {})
            )
            fixtures.append(fixture)
        
        return fixtures
    
    @classmethod
    def load_all_fixtures(cls) -> List[Fixture]:
        """Load all available test fixtures."""
        all_fixtures = []
        
        for category_dir in cls.fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            for language_dir in category_dir.iterdir():
                if not language_dir.is_dir():
                    continue
                
                fixtures = cls.load_fixtures_for_language(language_dir)
                all_fixtures.extend(fixtures)
        
        return all_fixtures
    
    def test_all_languages(self):
        """Test all available languages."""
        fixtures = self.load_all_fixtures()
        
        if not fixtures:
            self.skipTest("No fixtures available")
        
        logger.info(f"Testing {len(fixtures)} fixtures")
        
        def progress_callback(result, current, total):
            status_symbol = "✓" if result.passed else "✗"
            logger.info(
                f"[{current}/{total}] {status_symbol} "
                f"{result.fixture.language}/{result.fixture.fixture_type} "
                f"({result.execution_time:.3f}s)"
            )
        
        results = self.executor.execute_fixtures(fixtures, progress_callback)
        self.__class__.results.extend(results)
        
        # Generate report
        report = TestReporter.generate_detailed_report(results)
        print(report)
        
        # Save JSON report to .tmp directory
        tmp_dir = PROJECT_ROOT / '.tmp'
        tmp_dir.mkdir(exist_ok=True)
        report_path = tmp_dir / 'test_results.json'
        TestReporter.save_json_report(results, report_path)
        logger.info(f"Report saved to {report_path}")
        
        # Check for failures
        failed = [r for r in results if r.failed or r.status == Status.ERROR]
        if failed:
            self.fail(f"{len(failed)} tests failed. See report for details.")
    
    def _test_category(self, category: str):
        """Test all languages in a specific category. (Helper method, not a test)"""
        category_dir = self.fixtures_dir / category
        if not category_dir.exists():
            self.skipTest(f"Category {category} not found")
        
        fixtures = []
        for language_dir in category_dir.iterdir():
            if language_dir.is_dir():
                fixtures.extend(self.load_fixtures_for_language(language_dir))
        
        if not fixtures:
            self.skipTest(f"No fixtures in category {category}")
        
        results = self.executor.execute_fixtures(fixtures)
        self.__class__.results.extend(results)
        
        failed = [r for r in results if r.failed or r.status == Status.ERROR]
        if failed:
            self.fail(f"{len(failed)} tests failed in category {category}")
    
    def _test_language(self, category: str, language: str):
        """Test a specific language. (Helper method, not a test)"""
        language_dir = self.fixtures_dir / category / language
        if not language_dir.exists():
            self.skipTest(f"Language {language} not found in category {category}")
        
        fixtures = self.load_fixtures_for_language(language_dir)
        
        if not fixtures:
            self.skipTest(f"No fixtures for {language}")
        
        results = self.executor.execute_fixtures(fixtures)
        self.__class__.results.extend(results)
        
        for result in results:
            with self.subTest(fixture_type=result.fixture.fixture_type):
                if result.failed:
                    self.fail(result.error_message)
                elif result.status == Status.ERROR:
                    self.fail(f"Error: {result.error_message}")


def main():
    """Main entry point for standalone execution."""
    import argparse
    
    parser = argparse.ArgumentParser(description='E2E Line Counting Tests')
    parser.add_argument('--category', help='Test specific category')
    parser.add_argument('--language', help='Test specific language')
    parser.add_argument('--parallel', action='store_true', default=True,
                       help='Run tests in parallel')
    parser.add_argument('--workers', type=int, default=4,
                       help='Number of parallel workers')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    if args.language and args.category:
        # Test specific language - create wrapper test
        test = TestE2ELineCounting('test_all_languages')
        # Override the test method to call the specific language test
        original_test = test.test_all_languages
        test.test_all_languages = lambda: test._test_language(args.category, args.language)
        suite.addTest(test)
    elif args.category:
        # Test category - create wrapper test
        test = TestE2ELineCounting('test_all_languages')
        # Override the test method to call the category test
        original_test = test.test_all_languages
        test.test_all_languages = lambda: test._test_category(args.category)
        suite.addTest(test)
    else:
        # Test all
        suite.addTest(TestE2ELineCounting('test_all_languages'))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2 if args.verbose else 1)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(main())