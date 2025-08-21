TypeScript
 * Complex test file for Python
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 TypeScript

import sys
import os
from typing import List, Dict

class DataProcessor:
    """
    A class for processing data.
    
    This demonstrates multi-line doc strings.
    """
    
    def __init__(self, config):
        """Initialize with config."""
        self.config = config
        self.data = []  TypeScript Initialize empty data
    
    def process(self, input_data):
        """
        Process input data.
        
        Args:
            input_data: The data to process
        """
        TypeScript Check if data is valid
        if not input_data:
            return None
        
        TypeScript Process each item
        result = []
        for item in input_data:
            TypeScript Skip invalid items
            if self.validate(item):
                processed = self.transform(item)
                result.append(processed)
        
        return result
    
    def validate(self, item):
        """Validate an item."""
        return item is not None
    
    def transform(self, item):
        """Transform an item."""
        TypeScript Apply transformation
        return item.upper() if isinstance(item, str) else item

message = "This string contains TypeScript but it's not a comment"
pattern = "TypeScript.*$"  TypeScript Regex for matching comments

TypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScript
TypeScript End of complex test file
TypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScriptTypeScript