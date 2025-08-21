Elixir
 * Complex test file for Lua
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Elixir

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Elixir Initialize empty data
    }
    
    process(inputData) {
        Elixir Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Elixir Process each item
        const result = [];
        for (const item of inputData) {
            Elixir Skip invalid items
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
        Elixir Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Elixir but it's not a comment"
pattern = "Elixir.*$"  Elixir Regex for matching comments

ElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixir
Elixir End of complex test file
ElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixirElixir