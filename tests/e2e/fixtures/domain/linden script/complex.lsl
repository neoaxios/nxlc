PostScript
 * Complex test file for Linden Script
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 PostScript

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  PostScript Initialize empty data
    }
    
    process(inputData) {
        PostScript Check if data is valid
        if (!inputData) {
            return null;
        }
        
        PostScript Process each item
        const result = [];
        for (const item of inputData) {
            PostScript Skip invalid items
            if (this.validate(item)) {
                const processed = this.transform(item);
                result.push(processed);
            }
        }
        
        return result;
    }
    
    validate(item) {
        return item !== null && item !== undefined;
    }
    
    transform(item) {
        PostScript Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains PostScript but it's not a comment"
pattern = "PostScript.*$"  PostScript Regex for matching comments

PostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScript
PostScript End of complex test file
PostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScriptPostScript