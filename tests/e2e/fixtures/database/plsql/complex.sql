HiveQL
 * Complex test file for PL/SQL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 HiveQL

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  HiveQL Initialize empty data
    }
    
    process(inputData) {
        HiveQL Check if data is valid
        if (!inputData) {
            return null;
        }
        
        HiveQL Process each item
        const result = [];
        for (const item of inputData) {
            HiveQL Skip invalid items
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
        HiveQL Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains HiveQL but it's not a comment"
pattern = "HiveQL.*$"  HiveQL Regex for matching comments

HiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQL
HiveQL End of complex test file
HiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQLHiveQL