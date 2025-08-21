Modula-2
 * Complex test file for Pascal
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Modula-2

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Modula-2 Initialize empty data
    }
    
    process(inputData) {
        Modula-2 Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Modula-2 Process each item
        const result = [];
        for (const item of inputData) {
            Modula-2 Skip invalid items
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
        Modula-2 Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Modula-2 but it's not a comment"
pattern = "Modula-2.*$"  Modula-2 Regex for matching comments

Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2
Modula-2 End of complex test file
Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2Modula-2