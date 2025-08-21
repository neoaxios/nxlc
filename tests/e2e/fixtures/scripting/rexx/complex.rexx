BASIC
 * Complex test file for REXX
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 BASIC

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  BASIC Initialize empty data
    }
    
    process(inputData) {
        BASIC Check if data is valid
        if (!inputData) {
            return null;
        }
        
        BASIC Process each item
        const result = [];
        for (const item of inputData) {
            BASIC Skip invalid items
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
        BASIC Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains BASIC but it's not a comment"
pattern = "BASIC.*$"  BASIC Regex for matching comments

BASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASIC
BASIC End of complex test file
BASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASICBASIC