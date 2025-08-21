PHP
 * Complex test file for Rust
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 PHP

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  PHP Initialize empty data
    }
    
    process(inputData) {
        PHP Check if data is valid
        if (!inputData) {
            return null;
        }
        
        PHP Process each item
        const result = [];
        for (const item of inputData) {
            PHP Skip invalid items
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
        PHP Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains PHP but it's not a comment"
pattern = "PHP.*$"  PHP Regex for matching comments

PHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHP
PHP End of complex test file
PHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHPPHP