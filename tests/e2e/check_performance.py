#!/usr/bin/env python3
"""
Performance Regression Checker for E2E Tests

Compares current test performance against baseline and detects regressions.
"""

import json
import sys
from pathlib import Path
from typing import Dict, Tuple
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PerformanceChecker:
    """Checks for performance regressions in test execution."""
    
    def __init__(self, baseline_path: Path, results_path: Path):
        """Initialize with paths to baseline and results files."""
        self.baseline_path = baseline_path
        self.results_path = results_path
    
    def load_baseline(self) -> Dict:
        """Load performance baseline data."""
        if not self.baseline_path.exists():
            logger.warning(f"Baseline file not found: {self.baseline_path}")
            return {}
        
        with open(self.baseline_path, 'r') as f:
            return json.load(f)
    
    def load_results(self) -> Dict:
        """Load current test results."""
        if not self.results_path.exists():
            raise FileNotFoundError(f"Results file not found: {self.results_path}")
        
        with open(self.results_path, 'r') as f:
            return json.load(f)
    
    def check_regression(self, threshold_percent: float = 20.0) -> Tuple[bool, Dict]:
        """
        Check for performance regression.
        
        Returns:
            (has_regression, details)
        """
        baseline = self.load_baseline()
        results = self.load_results()
        
        if not baseline or 'baselines' not in baseline:
            logger.info("No baseline data available for comparison")
            return False, {}
        
        summary = results.get('summary', {})
        baselines = baseline.get('baselines', {})
        thresholds = baselines.get('thresholds', {})
        
        regression_threshold = thresholds.get('regression_percentage', threshold_percent)
        
        details = {
            'current': {},
            'baseline': {},
            'regressions': []
        }
        
        # Check average execution time
        current_avg_time = summary.get('average_execution_time', 0)
        baseline_avg_time = baselines.get('overall', {}).get('avg_execution_time_ms', 0) / 1000.0
        
        details['current']['avg_execution_time'] = current_avg_time
        details['baseline']['avg_execution_time'] = baseline_avg_time
        
        if baseline_avg_time > 0:
            time_increase_percent = ((current_avg_time - baseline_avg_time) / baseline_avg_time) * 100
            
            if time_increase_percent > regression_threshold:
                details['regressions'].append({
                    'metric': 'average_execution_time',
                    'baseline': baseline_avg_time,
                    'current': current_avg_time,
                    'increase_percent': time_increase_percent,
                    'threshold': regression_threshold
                })
        
        # Check total execution time
        current_total_time = summary.get('total_execution_time', 0)
        baseline_total_time = baselines.get('overall', {}).get('total_execution_time_s', 0)
        
        details['current']['total_execution_time'] = current_total_time
        details['baseline']['total_execution_time'] = baseline_total_time
        
        if baseline_total_time > 0:
            total_time_increase = ((current_total_time - baseline_total_time) / baseline_total_time) * 100
            
            if total_time_increase > regression_threshold:
                details['regressions'].append({
                    'metric': 'total_execution_time',
                    'baseline': baseline_total_time,
                    'current': current_total_time,
                    'increase_percent': total_time_increase,
                    'threshold': regression_threshold
                })
        
        # Check pass rate
        current_pass_rate = summary.get('pass_rate', 100)
        min_pass_rate = thresholds.get('min_pass_rate', 99.5)
        
        details['current']['pass_rate'] = current_pass_rate
        details['baseline']['min_pass_rate'] = min_pass_rate
        
        if current_pass_rate < min_pass_rate:
            details['regressions'].append({
                'metric': 'pass_rate',
                'baseline': min_pass_rate,
                'current': current_pass_rate,
                'threshold': min_pass_rate
            })
        
        has_regression = len(details['regressions']) > 0
        
        return has_regression, details
    
    def generate_report(self, details: Dict) -> str:
        """Generate a performance report."""
        lines = []
        lines.append("=" * 60)
        lines.append("PERFORMANCE REGRESSION CHECK")
        lines.append("=" * 60)
        
        lines.append("\nCurrent Performance:")
        for metric, value in details.get('current', {}).items():
            lines.append(f"  {metric}: {value:.3f}")
        
        lines.append("\nBaseline Performance:")
        for metric, value in details.get('baseline', {}).items():
            lines.append(f"  {metric}: {value:.3f}")
        
        regressions = details.get('regressions', [])
        if regressions:
            lines.append("\n⚠️  PERFORMANCE REGRESSIONS DETECTED:")
            for reg in regressions:
                lines.append(f"\n  {reg['metric']}:")
                lines.append(f"    Baseline: {reg['baseline']:.3f}")
                lines.append(f"    Current: {reg['current']:.3f}")
                if 'increase_percent' in reg:
                    lines.append(f"    Increase: {reg['increase_percent']:.1f}%")
                lines.append(f"    Threshold: {reg['threshold']:.1f}%")
        else:
            lines.append("\n✅ No performance regressions detected")
        
        lines.append("\n" + "=" * 60)
        return "\n".join(lines)
    
    def update_baseline(self, new_baseline_data: Dict):
        """Update the baseline with new performance data."""
        baseline = self.load_baseline()
        
        # Update baseline metrics
        if 'baselines' not in baseline:
            baseline['baselines'] = {}
        
        results = self.load_results()
        summary = results.get('summary', {})
        
        # Update overall metrics
        baseline['baselines']['overall'] = {
            'avg_execution_time_ms': summary.get('average_execution_time', 0) * 1000,
            'total_execution_time_s': summary.get('total_execution_time', 0),
            'total_fixtures': summary.get('total', 0)
        }
        
        # Save updated baseline
        with open(self.baseline_path, 'w') as f:
            json.dump(baseline, f, indent=2)
        
        logger.info(f"Baseline updated: {self.baseline_path}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Check for performance regressions')
    parser.add_argument('--baseline', '-b', type=Path,
                       default=Path(__file__).parent / 'performance_baseline.json',
                       help='Path to baseline file')
    parser.add_argument('--results', '-r', type=Path,
                       default=Path(__file__).parent / 'test_results.json',
                       help='Path to test results file')
    parser.add_argument('--threshold', '-t', type=float, default=20.0,
                       help='Regression threshold percentage (default: 20)')
    parser.add_argument('--update', action='store_true',
                       help='Update baseline with current results')
    parser.add_argument('--quiet', '-q', action='store_true',
                       help='Quiet mode - only report failures')
    
    args = parser.parse_args()
    
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    
    checker = PerformanceChecker(args.baseline, args.results)
    
    if args.update:
        checker.update_baseline({})
        print("Baseline updated with current performance metrics")
        return 0
    
    try:
        has_regression, details = checker.check_regression(args.threshold)
        
        if not args.quiet or has_regression:
            report = checker.generate_report(details)
            print(report)
        
        if has_regression:
            logger.error("Performance regressions detected!")
            return 1
        else:
            if not args.quiet:
                logger.info("Performance check passed")
            return 0
    
    except Exception as e:
        logger.error(f"Error checking performance: {e}")
        return 2


if __name__ == '__main__':
    sys.exit(main())