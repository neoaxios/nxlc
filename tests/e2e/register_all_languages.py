#!/usr/bin/env python3
"""
Register all 119 NXLC-supported languages for fixture generation.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from generate_fixtures import LanguageDefinition, CommentStyle, LanguageRegistry


def register_all_nxlc_languages():
    """Register all 119 languages supported by NXLC."""
    
    # Extract language definitions from nxlc.py
    nxlc_path = Path(__file__).parent.parent.parent / 'src' / 'nxlc.py'
    with open(nxlc_path, 'r') as f:
        content = f.read()
    
    # Parse LANGUAGE_EXTENSIONS and COMMENT_PATTERNS from source
    import re
    import ast
    
    # Find LANGUAGE_EXTENSIONS
    lang_ext_match = re.search(r'LANGUAGE_EXTENSIONS\s*=\s*(\{[^}]+(?:\{[^}]*\}[^}]*)*\})', content, re.DOTALL)
    if not lang_ext_match:
        raise ValueError("Could not find LANGUAGE_EXTENSIONS in nxlc.py")
    
    # Find COMMENT_PATTERNS  
    comment_pat_match = re.search(r'COMMENT_PATTERNS\s*=\s*(\{[^}]+(?:\{[^}]*\}[^}]*)*\})', content, re.DOTALL)
    if not comment_pat_match:
        raise ValueError("Could not find COMMENT_PATTERNS in nxlc.py")
    
    # Safely evaluate the dictionaries
    try:
        # Replace Python constants that ast.literal_eval can't handle
        lang_ext_str = lang_ext_match.group(1)
        lang_ext_str = lang_ext_str.replace('Makefile', '"Makefile"')
        lang_ext_str = lang_ext_str.replace('makefile', '"makefile"')
        lang_ext_str = lang_ext_str.replace('GNUmakefile', '"GNUmakefile"')
        lang_ext_str = lang_ext_str.replace('Dockerfile', '"Dockerfile"')
        lang_ext_str = lang_ext_str.replace('README', '"README"')
        
        LANGUAGE_EXTENSIONS = ast.literal_eval(lang_ext_str)
        COMMENT_PATTERNS = ast.literal_eval(comment_pat_match.group(1))
    except Exception as e:
        print(f"Error parsing language definitions: {e}")
        # Fall back to manual definitions
        LANGUAGE_EXTENSIONS = {}
        COMMENT_PATTERNS = {}
    
    # Categories for organization
    categories = {
        'Python': 'common', 'JavaScript': 'common', 'TypeScript': 'common', 'Java': 'common',
        'C': 'common', 'C++': 'common', 'C#': 'common', 'Go': 'common', 'Rust': 'common',
        'Ruby': 'common', 'PHP': 'common', 'Swift': 'common', 'Kotlin': 'common',
        'Scala': 'common', 'Dart': 'common',
        
        'HTML': 'web', 'CSS': 'web', 'Vue': 'web', 'Svelte': 'web', 'XAML': 'web',
        'QML': 'web', 'HAML': 'web', 'Slim': 'web', 'Pug': 'web', 'Handlebars': 'web',
        'Mustache': 'web', 'Jinja2': 'web', 'Liquid': 'web', 'Smarty': 'web', 'Twig': 'web',
        'ERB': 'web',
        
        'Assembly': 'systems', 'Zig': 'systems', 'Nim': 'systems', 'Crystal': 'systems',
        
        'Shell': 'scripting', 'PowerShell': 'scripting', 'Perl': 'scripting', 'Lua': 'scripting',
        'TCL': 'scripting', 'REXX': 'scripting',
        
        'SQL': 'database', 'PL/SQL': 'database', 'CQL': 'database', 'HiveQL': 'database',
        'Neo4j Cypher': 'database',
        
        'COBOL': 'legacy', 'FORTRAN': 'legacy', 'Pascal': 'legacy', 'Ada': 'legacy',
        'Modula-2': 'legacy', 'Modula-3': 'legacy', 'Oberon': 'legacy', 'ALGOL': 'legacy',
        'PL/I': 'legacy', 'RPG': 'legacy', 'JCL': 'legacy', 'BASIC': 'legacy',
        'Visual Basic': 'legacy',
        
        'Markdown': 'markup', 'YAML': 'markup', 'JSON': 'markup', 'XML': 'markup',
        'TOML': 'markup', 'AsciiDoc': 'markup', 'ReStructuredText': 'markup',
        'Org Mode': 'markup', 'MediaWiki': 'markup', 'Textile': 'markup', 'Creole': 'markup',
        'SVG': 'markup', 'KML': 'markup', 'RSS': 'markup', 'Atom': 'markup', 'OPML': 'markup',
        'RDF': 'markup', 'WSDL': 'markup', 'XSD': 'markup',
        
        'Makefile': 'config', 'Dockerfile': 'config', 'Configuration': 'config', 'INI': 'config',
        'Properties': 'config', 'Plist': 'config', 'README': 'config', 'Text': 'config',
    }
    
    # Register each language from NXLC
    count = 0
    for lang_name in LANGUAGE_EXTENSIONS.keys():
        extensions = LANGUAGE_EXTENSIONS.get(lang_name, [])
        comment_patterns = COMMENT_PATTERNS.get(lang_name, {})
        
        # Determine category
        category = categories.get(lang_name, 'domain')
        
        # Create comment style
        single_line = comment_patterns.get('single', [])
        multi_start = comment_patterns.get('multi_start', [])
        multi_end = comment_patterns.get('multi_end', [])
        
        comment_style = CommentStyle(
            single_line=single_line[0] if single_line else None,
            multi_line_start=multi_start[0] if multi_start else None,
            multi_line_end=multi_end[0] if multi_end else None
        )
        
        # Special handling for languages with multiple comment styles
        if lang_name == 'Python':
            comment_style.doc_string_delimiters = ['"""', "'''"]
        
        # Check for indent-based languages
        indent_based = lang_name in ['Python', 'HAML', 'Slim', 'Pug', 'YAML']
        
        # Create and register language definition
        lang_def = LanguageDefinition(
            name=lang_name,
            category=category,
            extensions=extensions[:5] if extensions else ['.txt'],  # Limit extensions for testing
            comment_style=comment_style,
            indent_based=indent_based
        )
        
        LanguageRegistry.register(lang_def)
        count += 1
    
    # Handle any missing languages by adding them with defaults
    missing_languages = {
        'Haskell': ('.hs', 'functional', '--', '{-', '-}'),
        'Elixir': ('.ex', 'functional', '#', None, None),
        'Clojure': ('.clj', 'functional', ';', None, None),
        'F#': ('.fs', 'functional', '//', '(*', '*)'),
        'Erlang': ('.erl', 'functional', '%', None, None),
        'R': ('.r', 'scientific', '#', None, None),
        'Julia': ('.jl', 'scientific', '#', '#=', '=#'),
        'Verilog': ('.v', 'domain', '//', '/*', '*/'),
        'VHDL': ('.vhd', 'domain', '--', None, None),
        'SystemVerilog': ('.sv', 'domain', '//', '/*', '*/'),
        'SPICE': ('.sp', 'domain', '*', None, None),
        'AutoLISP': ('.lsp', 'domain', ';', None, None),
        'Octave': ('.m', 'scientific', '#', '%{', '%}'),
        'Mathematica': ('.nb', 'scientific', None, '(*', '*)'),
        'Maple': ('.mpl', 'scientific', '#', None, None),
        'Stata': ('.do', 'scientific', '*', '/*', '*/'),
        'SAS': ('.sas', 'scientific', '*', '/*', '*/'),
        'SPSS': ('.sps', 'scientific', '*', '/*', '*/'),
        'GDScript': ('.gd', 'domain', '#', None, None),
        'UnrealScript': ('.uc', 'domain', '//', '/*', '*/'),
        'Linden Script': ('.lsl', 'domain', '//', '/*', '*/'),
        'OpenSCAD': ('.scad', 'domain', '//', '/*', '*/'),
        'PostScript': ('.ps', 'domain', '%', None, None),
        'TeX': ('.tex', 'markup', '%', None, None),
        'BibTeX': ('.bib', 'markup', '%', None, None),
        'Gnuplot': ('.gp', 'domain', '#', None, None),
        'DOT': ('.dot', 'domain', '//', '/*', '*/'),
        'PlantUML': ('.puml', 'domain', "'", "/'", "'/"),
        'Mermaid': ('.mmd', 'domain', '%%', None, None),
        'Protocol Buffers': ('.proto', 'domain', '//', '/*', '*/'),
        'Thrift': ('.thrift', 'domain', '//', '/*', '*/'),
        'Avro': ('.avsc', 'domain', None, None, None),
        'Glade': ('.glade', 'markup', None, '<!--', '-->'),
    }
    
    for lang_name, (ext, cat, single, m_start, m_end) in missing_languages.items():
        if lang_name not in LanguageRegistry._languages:
            LanguageRegistry.register(LanguageDefinition(
                name=lang_name,
                category=cat,
                extensions=[ext],
                comment_style=CommentStyle(
                    single_line=single,
                    multi_line_start=m_start,
                    multi_line_end=m_end
                )
            ))
            count += 1
    
    return count


if __name__ == '__main__':
    count = register_all_nxlc_languages()
    print(f"Registered {count} languages")
    
    # List by category
    by_category = LanguageRegistry.list_by_category()
    for category, languages in sorted(by_category.items()):
        print(f"\n{category}: {len(languages)} languages")
        for lang in sorted(languages)[:5]:  # Show first 5
            print(f"  - {lang}")
        if len(languages) > 5:
            print(f"  ... and {len(languages) - 5} more")