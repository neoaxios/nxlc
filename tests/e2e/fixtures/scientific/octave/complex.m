Maple
 * Complex test file for Octave
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Maple

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Maple Initialize empty data
    }
    
    process(inputData) {
        Maple Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Maple Process each item
        const result = [];
        for (const item of inputData) {
            Maple Skip invalid items
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
        Maple Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Maple but it's not a comment"
pattern = "Maple.*$"  Maple Regex for matching comments

MapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMaple
Maple End of complex test file
MapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMapleMaple