HTML
 * Complex test file for PowerShell
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 HTML

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  HTML Initialize empty data
    }
    
    process(inputData) {
        HTML Check if data is valid
        if (!inputData) {
            return null;
        }
        
        HTML Process each item
        const result = [];
        for (const item of inputData) {
            HTML Skip invalid items
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
        HTML Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains HTML but it's not a comment"
pattern = "HTML.*$"  HTML Regex for matching comments

HTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTML
HTML End of complex test file
HTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTMLHTML