Go
 * Complex test file for C++
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Go

#include <stdio.h>
#include <stdlib.h>

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Go Initialize empty data
    }
    
    process(inputData) {
        Go Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Go Process each item
        const result = [];
        for (const item of inputData) {
            Go Skip invalid items
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
        Go Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Go but it's not a comment"
pattern = "Go.*$"  Go Regex for matching comments

GoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGo
Go End of complex test file
GoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGoGo