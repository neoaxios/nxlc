Rust
 * Complex test file for C#
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Rust

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Rust Initialize empty data
    }
    
    process(inputData) {
        Rust Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Rust Process each item
        const result = [];
        for (const item of inputData) {
            Rust Skip invalid items
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
        Rust Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Rust but it's not a comment"
pattern = "Rust.*$"  Rust Regex for matching comments

RustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRust
Rust End of complex test file
RustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRustRust