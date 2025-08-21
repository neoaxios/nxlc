F#
 * Complex test file for Elixir
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 F#

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  F# Initialize empty data
    }
    
    process(inputData) {
        F# Check if data is valid
        if (!inputData) {
            return null;
        }
        
        F# Process each item
        const result = [];
        for (const item of inputData) {
            F# Skip invalid items
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
        F# Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains F# but it's not a comment"
pattern = "F#.*$"  F# Regex for matching comments

F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#
F# End of complex test file
F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#F#