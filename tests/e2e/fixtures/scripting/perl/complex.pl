Haskell
 * Complex test file for Perl
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Haskell

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Haskell Initialize empty data
    }
    
    process(inputData) {
        Haskell Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Haskell Process each item
        const result = [];
        for (const item of inputData) {
            Haskell Skip invalid items
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
        Haskell Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Haskell but it's not a comment"
pattern = "Haskell.*$"  Haskell Regex for matching comments

HaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskell
Haskell End of complex test file
HaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskellHaskell