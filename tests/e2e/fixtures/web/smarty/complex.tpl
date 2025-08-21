ERB
 * Complex test file for Smarty
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 ERB

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  ERB Initialize empty data
    }
    
    process(inputData) {
        ERB Check if data is valid
        if (!inputData) {
            return null;
        }
        
        ERB Process each item
        const result = [];
        for (const item of inputData) {
            ERB Skip invalid items
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
        ERB Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains ERB but it's not a comment"
pattern = "ERB.*$"  ERB Regex for matching comments

ERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERB
ERB End of complex test file
ERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERBERB