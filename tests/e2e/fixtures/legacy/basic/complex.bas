Visual Basic
 * Complex test file for BASIC
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Visual Basic

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Visual Basic Initialize empty data
    }
    
    process(inputData) {
        Visual Basic Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Visual Basic Process each item
        const result = [];
        for (const item of inputData) {
            Visual Basic Skip invalid items
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
        Visual Basic Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Visual Basic but it's not a comment"
pattern = "Visual Basic.*$"  Visual Basic Regex for matching comments

Visual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual Basic
Visual Basic End of complex test file
Visual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual BasicVisual Basic