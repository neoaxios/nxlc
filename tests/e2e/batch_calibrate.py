#!/usr/bin/env python3
"""
Batch calibration for all fixture expected values.
"""

import sys
from pathlib import Path
import logging
import json

sys.path.insert(0, str(Path(__file__).parent))
from calibrate_fixtures import NXLCCalibrator

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def calibrate_all_fixtures(fixtures_dir: Path, batch_size: int = 10):
    """Calibrate all fixtures in batches."""
    calibrator = NXLCCalibrator()
    
    # Find all language directories
    lang_dirs = []
    for category_dir in fixtures_dir.iterdir():
        if not category_dir.is_dir():
            continue
        for lang_dir in category_dir.iterdir():
            if lang_dir.is_dir() and (lang_dir / 'expected.json').exists():
                lang_dirs.append(lang_dir)
    
    logger.info(f"Found {len(lang_dirs)} language directories to calibrate")
    
    calibrated = 0
    failed = []
    
    # Process in batches
    for i in range(0, len(lang_dirs), batch_size):
        batch = lang_dirs[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(len(lang_dirs)-1)//batch_size + 1}")
        
        for lang_dir in batch:
            try:
                if calibrator.calibrate_language(lang_dir, dry_run=False):
                    calibrated += 1
                    logger.info(f"  ✓ {lang_dir.parent.name}/{lang_dir.name}")
                else:
                    logger.info(f"  - {lang_dir.parent.name}/{lang_dir.name} (no changes)")
            except Exception as e:
                failed.append((lang_dir, str(e)))
                logger.error(f"  ✗ {lang_dir.parent.name}/{lang_dir.name}: {e}")
    
    return calibrated, failed


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch calibrate fixture expected values')
    parser.add_argument('--fixtures', '-f', type=Path,
                       default=Path(__file__).parent / 'fixtures',
                       help='Path to fixtures directory')
    parser.add_argument('--batch-size', '-b', type=int, default=20,
                       help='Number of languages to process per batch')
    
    args = parser.parse_args()
    
    logger.info("Starting batch calibration...")
    calibrated, failed = calibrate_all_fixtures(args.fixtures, args.batch_size)
    
    # Summary
    print("\n" + "=" * 50)
    print("CALIBRATION SUMMARY")
    print("=" * 50)
    print(f"Total languages: {calibrated + len(failed)}")
    print(f"Successfully calibrated: {calibrated}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed calibrations:")
        for lang_dir, error in failed[:10]:
            print(f"  - {lang_dir}: {error}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")
    
    return 0 if len(failed) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())