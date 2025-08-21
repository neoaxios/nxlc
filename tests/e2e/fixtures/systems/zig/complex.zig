Crystal
 * Complex test file for Zig
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Crystal

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Crystal Initialize empty data
    }
    
    process(inputData) {
        Crystal Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Crystal Process each item
        const result = [];
        for (const item of inputData) {
            Crystal Skip invalid items
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
        Crystal Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Crystal but it's not a comment"
pattern = "Crystal.*$"  Crystal Regex for matching comments

CrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystal
Crystal End of complex test file
CrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystalCrystal