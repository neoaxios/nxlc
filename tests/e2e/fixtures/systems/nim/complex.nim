Scala
 * Complex test file for Nim
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Scala

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Scala Initialize empty data
    }
    
    process(inputData) {
        Scala Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Scala Process each item
        const result = [];
        for (const item of inputData) {
            Scala Skip invalid items
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
        Scala Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Scala but it's not a comment"
pattern = "Scala.*$"  Scala Regex for matching comments

ScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScala
Scala End of complex test file
ScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScalaScala