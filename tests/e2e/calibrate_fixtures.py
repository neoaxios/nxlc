#!/usr/bin/env python3
"""
Calibrate fixture expected values based on actual NXLC output.

This tool runs NXLC on each fixture and updates the expected.json files
with the actual counts reported by NXLC.
"""

import json
import sys
from pathlib import Path
import subprocess
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add project root to path
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT / 'src'))


class NXLCCalibrator:
    """Calibrates fixture expected values using actual NXLC output."""
    
    def __init__(self, nxlc_path: Path = None):
        """Initialize calibrator."""
        if nxlc_path:
            self.nxlc_path = nxlc_path
        else:
            self.nxlc_path = PROJECT_ROOT / 'src' / 'nxlc.py'
        
        if not self.nxlc_path.exists():
            raise FileNotFoundError(f"NXLC not found at {self.nxlc_path}")
    
    def get_actual_counts(self, file_path: Path) -> dict:
        """Get actual line counts from NXLC for a file."""
        import tempfile
        import shutil
        
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Copy file to temp directory
                tmp_file = Path(tmpdir) / file_path.name
                shutil.copy2(file_path, tmp_file)
                
                # Run NXLC
                result = subprocess.run(
                    [sys.executable, str(self.nxlc_path), tmpdir, '--no-git', '--no-color'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode != 0:
                    logger.error(f"NXLC failed for {file_path}: {result.stderr}")
                    return None
                
                # Parse output
                return self._parse_nxlc_output(result.stdout)
        
        except Exception as e:
            logger.error(f"Error processing {file_path}: {e}")
            return None
    
    def _parse_nxlc_output(self, output: str) -> dict:
        """Parse NXLC output to extract counts."""
        lines = output.strip().split('\n')
        
        in_table = False
        for line in lines:
            if not line.strip() or '-' * 10 in line:
                continue
            
            if 'Language' in line and 'Files' in line and 'Total' in line:
                in_table = True
                continue
            
            if in_table:
                if line.strip().startswith('Total'):
                    continue
                
                parts = line.split()
                if len(parts) >= 5:
                    try:
                        total_lines = int(parts[2])
                        code_count = int(parts[3])
                        comment_count = int(parts[4])
                        blank_count = total_lines - code_count - comment_count
                        
                        return {
                            'total': total_lines,
                            'code': code_count,
                            'comments': comment_count,
                            'blank': blank_count
                        }
                    except (ValueError, IndexError):
                        continue
        
        return None
    
    def calibrate_language(self, lang_dir: Path, dry_run: bool = False) -> bool:
        """Calibrate expected values for a language."""
        expected_file = lang_dir / 'expected.json'
        
        if not expected_file.exists():
            logger.warning(f"No expected.json in {lang_dir}")
            return False
        
        # Load current expected data
        with open(expected_file, 'r') as f:
            expected_data = json.load(f)
        
        language = expected_data.get('language', lang_dir.name)
        logger.info(f"Calibrating {language}...")
        
        updated = False
        
        # Process each fixture type
        for fixture_type in ['simple', 'complex', 'edge_cases']:
            if fixture_type not in expected_data:
                continue
            
            fixture_info = expected_data[fixture_type]
            fixture_file = lang_dir / fixture_info['filename']
            
            if not fixture_file.exists():
                logger.warning(f"  Fixture {fixture_file} not found")
                continue
            
            # Get actual counts
            actual_counts = self.get_actual_counts(fixture_file)
            
            if actual_counts:
                # Compare with expected
                old_counts = {
                    'total': fixture_info.get('total', 0),
                    'code': fixture_info.get('code', 0),
                    'comments': fixture_info.get('comments', 0),
                    'blank': fixture_info.get('blank', 0)
                }
                
                if old_counts != actual_counts:
                    logger.info(f"  {fixture_type}: Updating counts")
                    logger.info(f"    Old: {old_counts}")
                    logger.info(f"    New: {actual_counts}")
                    
                    # Update expected data
                    fixture_info.update(actual_counts)
                    updated = True
                else:
                    logger.info(f"  {fixture_type}: Counts match ✓")
        
        # Save updated data
        if updated and not dry_run:
            with open(expected_file, 'w') as f:
                json.dump(expected_data, f, indent=2)
            logger.info(f"  Updated {expected_file}")
        elif updated and dry_run:
            logger.info(f"  Would update {expected_file} (dry run)")
        
        return updated
    
    def calibrate_all(self, fixtures_dir: Path, dry_run: bool = False) -> int:
        """Calibrate all fixtures."""
        updated_count = 0
        
        for category_dir in fixtures_dir.iterdir():
            if not category_dir.is_dir():
                continue
            
            for lang_dir in category_dir.iterdir():
                if not lang_dir.is_dir():
                    continue
                
                if self.calibrate_language(lang_dir, dry_run):
                    updated_count += 1
        
        return updated_count


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='Calibrate E2E test fixtures')
    parser.add_argument('--fixtures', '-f', type=Path,
                       default=Path(__file__).parent / 'fixtures',
                       help='Path to fixtures directory')
    parser.add_argument('--language', '-l',
                       help='Calibrate specific language only')
    parser.add_argument('--category', '-c',
                       help='Calibrate specific category only')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='Show what would be updated without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    calibrator = NXLCCalibrator()
    
    if args.language:
        # Find language directory
        found = False
        for category_dir in args.fixtures.iterdir():
            if not category_dir.is_dir():
                continue
            lang_dir = category_dir / args.language.lower()
            if lang_dir.exists():
                if calibrator.calibrate_language(lang_dir, args.dry_run):
                    print(f"Calibrated {args.language}")
                found = True
                break
        
        if not found:
            logger.error(f"Language '{args.language}' not found")
            return 1
    
    elif args.category:
        category_dir = args.fixtures / args.category
        if not category_dir.exists():
            logger.error(f"Category '{args.category}' not found")
            return 1
        
        updated = 0
        for lang_dir in category_dir.iterdir():
            if lang_dir.is_dir():
                if calibrator.calibrate_language(lang_dir, args.dry_run):
                    updated += 1
        
        print(f"Calibrated {updated} languages in category '{args.category}'")
    
    else:
        # Calibrate all
        updated = calibrator.calibrate_all(args.fixtures, args.dry_run)
        print(f"Calibrated {updated} languages")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())