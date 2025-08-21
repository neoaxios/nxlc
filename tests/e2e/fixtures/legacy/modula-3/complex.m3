ALGOL
 * Complex test file for Modula-3
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 ALGOL

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  ALGOL Initialize empty data
    }
    
    process(inputData) {
        ALGOL Check if data is valid
        if (!inputData) {
            return null;
        }
        
        ALGOL Process each item
        const result = [];
        for (const item of inputData) {
            ALGOL Skip invalid items
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
        ALGOL Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains ALGOL but it's not a comment"
pattern = "ALGOL.*$"  ALGOL Regex for matching comments

ALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOL
ALGOL End of complex test file
ALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOLALGOL