R
 * Complex test file for Scala
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 R

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  R Initialize empty data
    }
    
    process(inputData) {
        R Check if data is valid
        if (!inputData) {
            return null;
        }
        
        R Process each item
        const result = [];
        for (const item of inputData) {
            R Skip invalid items
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
        R Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains R but it's not a comment"
pattern = "R.*$"  R Regex for matching comments

RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
R End of complex test file
RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR