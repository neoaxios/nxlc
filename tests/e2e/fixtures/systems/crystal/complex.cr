Dart
 * Complex test file for Crystal
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Dart

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Dart Initialize empty data
    }
    
    process(inputData) {
        Dart Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Dart Process each item
        const result = [];
        for (const item of inputData) {
            Dart Skip invalid items
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
        Dart Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Dart but it's not a comment"
pattern = "Dart.*$"  Dart Regex for matching comments

DartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDart
Dart End of complex test file
DartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDartDart