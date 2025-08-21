Ruby
 * Complex test file for Go
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Ruby

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Ruby Initialize empty data
    }
    
    process(inputData) {
        Ruby Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Ruby Process each item
        const result = [];
        for (const item of inputData) {
            Ruby Skip invalid items
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
        Ruby Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Ruby but it's not a comment"
pattern = "Ruby.*$"  Ruby Regex for matching comments

RubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRuby
Ruby End of complex test file
RubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRubyRuby