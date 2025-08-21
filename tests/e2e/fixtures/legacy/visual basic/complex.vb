PL/SQL
 * Complex test file for Visual Basic
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 PL/SQL

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  PL/SQL Initialize empty data
    }
    
    process(inputData) {
        PL/SQL Check if data is valid
        if (!inputData) {
            return null;
        }
        
        PL/SQL Process each item
        const result = [];
        for (const item of inputData) {
            PL/SQL Skip invalid items
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
        PL/SQL Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains PL/SQL but it's not a comment"
pattern = "PL/SQL.*$"  PL/SQL Regex for matching comments

PL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQL
PL/SQL End of complex test file
PL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQLPL/SQL