Zig
 * Complex test file for F#
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Zig

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Zig Initialize empty data
    }
    
    process(inputData) {
        Zig Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Zig Process each item
        const result = [];
        for (const item of inputData) {
            Zig Skip invalid items
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
        Zig Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Zig but it's not a comment"
pattern = "Zig.*$"  Zig Regex for matching comments

ZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZig
Zig End of complex test file
ZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZigZig