Linden Script
 * Complex test file for GDScript
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Linden Script

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Linden Script Initialize empty data
    }
    
    process(inputData) {
        Linden Script Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Linden Script Process each item
        const result = [];
        for (const item of inputData) {
            Linden Script Skip invalid items
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
        Linden Script Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Linden Script but it's not a comment"
pattern = "Linden Script.*$"  Linden Script Regex for matching comments

Linden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden Script
Linden Script End of complex test file
Linden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden ScriptLinden Script