Swift
 * Complex test file for Ruby
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Swift

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Swift Initialize empty data
    }
    
    process(inputData) {
        Swift Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Swift Process each item
        const result = [];
        for (const item of inputData) {
            Swift Skip invalid items
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
        Swift Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Swift but it's not a comment"
pattern = "Swift.*$"  Swift Regex for matching comments

SwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwift
Swift End of complex test file
SwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwiftSwift