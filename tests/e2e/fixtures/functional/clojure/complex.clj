Erlang
 * Complex test file for Clojure
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Erlang

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Erlang Initialize empty data
    }
    
    process(inputData) {
        Erlang Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Erlang Process each item
        const result = [];
        for (const item of inputData) {
            Erlang Skip invalid items
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
        Erlang Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Erlang but it's not a comment"
pattern = "Erlang.*$"  Erlang Regex for matching comments

ErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlang
Erlang End of complex test file
ErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlangErlang