TCL
 * Complex test file for SPICE
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 TCL

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  TCL Initialize empty data
    }
    
    process(inputData) {
        TCL Check if data is valid
        if (!inputData) {
            return null;
        }
        
        TCL Process each item
        const result = [];
        for (const item of inputData) {
            TCL Skip invalid items
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
        TCL Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains TCL but it's not a comment"
pattern = "TCL.*$"  TCL Regex for matching comments

TCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCL
TCL End of complex test file
TCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCLTCL