GDScript
 * Complex test file for SAS
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 GDScript

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  GDScript Initialize empty data
    }
    
    process(inputData) {
        GDScript Check if data is valid
        if (!inputData) {
            return null;
        }
        
        GDScript Process each item
        const result = [];
        for (const item of inputData) {
            GDScript Skip invalid items
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
        GDScript Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains GDScript but it's not a comment"
pattern = "GDScript.*$"  GDScript Regex for matching comments

GDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScript
GDScript End of complex test file
GDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScriptGDScript