Svelte
 * Complex test file for Julia
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Svelte

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Svelte Initialize empty data
    }
    
    process(inputData) {
        Svelte Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Svelte Process each item
        const result = [];
        for (const item of inputData) {
            Svelte Skip invalid items
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
        Svelte Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Svelte but it's not a comment"
pattern = "Svelte.*$"  Svelte Regex for matching comments

SvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelte
Svelte End of complex test file
SvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelteSvelte