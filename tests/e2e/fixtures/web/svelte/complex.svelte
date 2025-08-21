COBOL
 * Complex test file for Svelte
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 COBOL

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  COBOL Initialize empty data
    }
    
    process(inputData) {
        COBOL Check if data is valid
        if (!inputData) {
            return null;
        }
        
        COBOL Process each item
        const result = [];
        for (const item of inputData) {
            COBOL Skip invalid items
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
        COBOL Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains COBOL but it's not a comment"
pattern = "COBOL.*$"  COBOL Regex for matching comments

COBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOL
COBOL End of complex test file
COBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOLCOBOL