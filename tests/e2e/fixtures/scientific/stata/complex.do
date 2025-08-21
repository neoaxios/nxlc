SPSS
 * Complex test file for Stata
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 SPSS

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  SPSS Initialize empty data
    }
    
    process(inputData) {
        SPSS Check if data is valid
        if (!inputData) {
            return null;
        }
        
        SPSS Process each item
        const result = [];
        for (const item of inputData) {
            SPSS Skip invalid items
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
        SPSS Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains SPSS but it's not a comment"
pattern = "SPSS.*$"  SPSS Regex for matching comments

SPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSS
SPSS End of complex test file
SPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSSSPSS