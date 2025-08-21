Pascal
 * Complex test file for COBOL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Pascal

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Pascal Initialize empty data
    }
    
    process(inputData) {
        Pascal Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Pascal Process each item
        const result = [];
        for (const item of inputData) {
            Pascal Skip invalid items
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
        Pascal Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Pascal but it's not a comment"
pattern = "Pascal.*$"  Pascal Regex for matching comments

PascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascal
Pascal End of complex test file
PascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascalPascal