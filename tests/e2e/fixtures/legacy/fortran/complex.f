Ada
 * Complex test file for FORTRAN
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Ada

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Ada Initialize empty data
    }
    
    process(inputData) {
        Ada Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Ada Process each item
        const result = [];
        for (const item of inputData) {
            Ada Skip invalid items
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
        Ada Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Ada but it's not a comment"
pattern = "Ada.*$"  Ada Regex for matching comments

AdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAda
Ada End of complex test file
AdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAdaAda