SAS
 * Complex test file for Maple
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 SAS

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  SAS Initialize empty data
    }
    
    process(inputData) {
        SAS Check if data is valid
        if (!inputData) {
            return null;
        }
        
        SAS Process each item
        const result = [];
        for (const item of inputData) {
            SAS Skip invalid items
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
        SAS Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains SAS but it's not a comment"
pattern = "SAS.*$"  SAS Regex for matching comments

SASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSAS
SAS End of complex test file
SASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSASSAS