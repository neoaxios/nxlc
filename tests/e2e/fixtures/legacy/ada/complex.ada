Modula-3
 * Complex test file for Ada
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Modula-3

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Modula-3 Initialize empty data
    }
    
    process(inputData) {
        Modula-3 Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Modula-3 Process each item
        const result = [];
        for (const item of inputData) {
            Modula-3 Skip invalid items
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
        Modula-3 Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Modula-3 but it's not a comment"
pattern = "Modula-3.*$"  Modula-3 Regex for matching comments

Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3
Modula-3 End of complex test file
Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3Modula-3