SPICE
 * Complex test file for VHDL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 SPICE

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  SPICE Initialize empty data
    }
    
    process(inputData) {
        SPICE Check if data is valid
        if (!inputData) {
            return null;
        }
        
        SPICE Process each item
        const result = [];
        for (const item of inputData) {
            SPICE Skip invalid items
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
        SPICE Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains SPICE but it's not a comment"
pattern = "SPICE.*$"  SPICE Regex for matching comments

SPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICE
SPICE End of complex test file
SPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICESPICE