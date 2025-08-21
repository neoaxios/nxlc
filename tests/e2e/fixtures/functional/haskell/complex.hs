Clojure
 * Complex test file for Haskell
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Clojure

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Clojure Initialize empty data
    }
    
    process(inputData) {
        Clojure Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Clojure Process each item
        const result = [];
        for (const item of inputData) {
            Clojure Skip invalid items
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
        Clojure Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Clojure but it's not a comment"
pattern = "Clojure.*$"  Clojure Regex for matching comments

ClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojure
Clojure End of complex test file
ClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojureClojure