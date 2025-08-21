Julia
 * Complex test file for Dart
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Julia

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Julia Initialize empty data
    }
    
    process(inputData) {
        Julia Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Julia Process each item
        const result = [];
        for (const item of inputData) {
            Julia Skip invalid items
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
        Julia Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Julia but it's not a comment"
pattern = "Julia.*$"  Julia Regex for matching comments

JuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJulia
Julia End of complex test file
JuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJuliaJulia