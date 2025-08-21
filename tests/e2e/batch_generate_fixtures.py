#!/usr/bin/env python3
"""
Batch fixture generator for all 119 NXLC languages.
Generates fixtures in batches to avoid memory issues.
"""

import sys
from pathlib import Path
import logging
import json

sys.path.insert(0, str(Path(__file__).parent))
from generate_fixtures import (
    LanguageDefinition, CommentStyle, LanguageRegistry,
    FixtureGenerator
)
from fixture_utils import get_language_definitions

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)


def extract_nxlc_languages():
    """Extract language definitions from nxlc module."""
    defs = get_language_definitions()
    return defs['languages'], defs['comment_patterns']


def categorize_language(lang_name):
    """Categorize a language based on its name."""
    categories = {
        'common': ['Python', 'JavaScript', 'TypeScript', 'Java', 'C', 'C++', 'C#', 
                  'Go', 'Rust', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Scala', 'Dart'],
        'web': ['HTML', 'CSS', 'Vue', 'Svelte', 'XAML', 'QML', 'HAML', 'Slim', 
                'Pug', 'Handlebars', 'Mustache', 'Jinja2', 'Liquid', 'Smarty', 'Twig', 'ERB'],
        'systems': ['Assembly', 'Zig', 'Nim', 'Crystal'],
        'scripting': ['Shell', 'PowerShell', 'Perl', 'Lua', 'TCL', 'REXX'],
        'database': ['SQL', 'PL/SQL', 'CQL', 'HiveQL', 'Neo4j Cypher'],
        'legacy': ['COBOL', 'FORTRAN', 'Pascal', 'Ada', 'Modula-2', 'Modula-3', 
                  'Oberon', 'ALGOL', 'PL/I', 'RPG', 'JCL', 'BASIC', 'Visual Basic'],
        'functional': ['Haskell', 'Elixir', 'Clojure', 'F#', 'Erlang'],
        'scientific': ['R', 'Julia', 'Octave', 'Mathematica', 'Maple', 'Stata', 'SAS', 'SPSS'],
        'markup': ['Markdown', 'YAML', 'JSON', 'XML', 'TOML', 'AsciiDoc', 'ReStructuredText',
                  'Org Mode', 'MediaWiki', 'Textile', 'Creole', 'SVG', 'KML', 'RSS', 
                  'Atom', 'OPML', 'RDF', 'WSDL', 'XSD', 'TeX', 'BibTeX'],
        'config': ['Makefile', 'Dockerfile', 'Configuration', 'INI', 'Properties', 
                  'Plist', 'README', 'Text'],
        'domain': []  # Everything else
    }
    
    for category, langs in categories.items():
        if lang_name in langs:
            return category
    return 'domain'


def register_language(lang_name, extensions, comment_patterns):
    """Register a single language with the fixture generator."""
    category = categorize_language(lang_name)
    
    # Get comment patterns
    patterns = comment_patterns.get(lang_name, {})
    single = patterns.get('single', [])
    multi_start = patterns.get('multi_start', [])
    multi_end = patterns.get('multi_end', [])
    
    # Create comment style
    comment_style = CommentStyle(
        single_line=single[0] if single else None,
        multi_line_start=multi_start[0] if multi_start else None,
        multi_line_end=multi_end[0] if multi_end else None
    )
    
    # Special cases
    if lang_name == 'Python':
        comment_style.doc_string_delimiters = ['"""', "'''"]
    
    # Determine if indent-based
    indent_based = lang_name in ['Python', 'YAML', 'HAML', 'Slim', 'Pug']
    
    # Create language definition
    lang_def = LanguageDefinition(
        name=lang_name,
        category=category,
        extensions=extensions[:3] if extensions else ['.txt'],  # Limit to 3 extensions
        comment_style=comment_style,
        indent_based=indent_based
    )
    
    LanguageRegistry.register(lang_def)
    return lang_def


def generate_fixtures_batch(languages, comment_patterns, output_dir, batch_size=10):
    """Generate fixtures in batches."""
    generator = FixtureGenerator(output_dir)
    
    lang_list = list(languages.keys())
    total = len(lang_list)
    generated = 0
    failed = []
    
    for i in range(0, total, batch_size):
        batch = lang_list[i:i+batch_size]
        logger.info(f"Processing batch {i//batch_size + 1}/{(total-1)//batch_size + 1}")
        
        # Clear registry for each batch to avoid memory buildup
        LanguageRegistry._languages.clear()
        
        for lang_name in batch:
            try:
                extensions = languages[lang_name]
                lang_def = register_language(lang_name, extensions, comment_patterns)
                
                if generator.generate_language_fixtures(lang_def, force=True):
                    generated += 1
                    logger.info(f"  ✓ {lang_name}")
                else:
                    logger.info(f"  - {lang_name} (skipped)")
                    
            except Exception as e:
                failed.append((lang_name, str(e)))
                logger.error(f"  ✗ {lang_name}: {e}")
    
    return generated, failed


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate fixtures for all NXLC languages')
    parser.add_argument('--output', '-o', type=Path,
                       default=Path(__file__).parent / 'fixtures',
                       help='Output directory')
    parser.add_argument('--batch-size', '-b', type=int, default=10,
                       help='Number of languages to process per batch')
    parser.add_argument('--list', '-l', action='store_true',
                       help='Just list languages without generating')
    
    args = parser.parse_args()
    
    # Extract language definitions
    logger.info("Extracting language definitions from nxlc.py...")
    languages, comment_patterns = extract_nxlc_languages()
    
    logger.info(f"Found {len(languages)} languages")
    
    if args.list:
        # Group by category and list
        by_category = {}
        for lang in languages.keys():
            cat = categorize_language(lang)
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(lang)
        
        print("\nLanguages by Category:")
        print("=" * 50)
        for category in sorted(by_category.keys()):
            langs = sorted(by_category[category])
            print(f"\n{category.upper()} ({len(langs)} languages):")
            for lang in langs:
                exts = languages[lang]
                print(f"  - {lang}: {', '.join(exts[:3])}")
        
        print(f"\nTotal: {len(languages)} languages")
        return 0
    
    # Generate fixtures
    logger.info(f"Generating fixtures in batches of {args.batch_size}...")
    generated, failed = generate_fixtures_batch(
        languages, comment_patterns, args.output, args.batch_size
    )
    
    # Summary
    print("\n" + "=" * 50)
    print("FIXTURE GENERATION SUMMARY")
    print("=" * 50)
    print(f"Total languages: {len(languages)}")
    print(f"Successfully generated: {generated}")
    print(f"Failed: {len(failed)}")
    
    if failed:
        print("\nFailed languages:")
        for lang, error in failed[:10]:  # Show first 10
            print(f"  - {lang}: {error}")
        if len(failed) > 10:
            print(f"  ... and {len(failed) - 10} more")
    
    # Save summary
    summary_file = args.output / 'generation_summary.json'
    with open(summary_file, 'w') as f:
        json.dump({
            'total': len(languages),
            'generated': generated,
            'failed': len(failed),
            'failed_languages': [lang for lang, _ in failed]
        }, f, indent=2)
    
    logger.info(f"Summary saved to {summary_file}")
    
    return 0 if len(failed) == 0 else 1


if __name__ == '__main__':
    sys.exit(main())