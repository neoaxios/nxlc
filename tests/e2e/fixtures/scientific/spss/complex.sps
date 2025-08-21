UnrealScript
 * Complex test file for SPSS
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 UnrealScript

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  UnrealScript Initialize empty data
    }
    
    process(inputData) {
        UnrealScript Check if data is valid
        if (!inputData) {
            return null;
        }
        
        UnrealScript Process each item
        const result = [];
        for (const item of inputData) {
            UnrealScript Skip invalid items
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
        UnrealScript Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains UnrealScript but it's not a comment"
pattern = "UnrealScript.*$"  UnrealScript Regex for matching comments

UnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScript
UnrealScript End of complex test file
UnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScriptUnrealScript