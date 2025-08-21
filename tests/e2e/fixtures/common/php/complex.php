Kotlin
 * Complex test file for PHP
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Kotlin

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Kotlin Initialize empty data
    }
    
    process(inputData) {
        Kotlin Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Kotlin Process each item
        const result = [];
        for (const item of inputData) {
            Kotlin Skip invalid items
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
        Kotlin Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Kotlin but it's not a comment"
pattern = "Kotlin.*$"  Kotlin Regex for matching comments

KotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlin
Kotlin End of complex test file
KotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlinKotlin