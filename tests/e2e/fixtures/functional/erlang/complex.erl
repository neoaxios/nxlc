Nim
 * Complex test file for Erlang
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Nim

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Nim Initialize empty data
    }
    
    process(inputData) {
        Nim Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Nim Process each item
        const result = [];
        for (const item of inputData) {
            Nim Skip invalid items
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
        Nim Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Nim but it's not a comment"
pattern = "Nim.*$"  Nim Regex for matching comments

NimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNim
Nim End of complex test file
NimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNimNim