Oberon
 * Complex test file for Modula-2
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Oberon

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Oberon Initialize empty data
    }
    
    process(inputData) {
        Oberon Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Oberon Process each item
        const result = [];
        for (const item of inputData) {
            Oberon Skip invalid items
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
        Oberon Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Oberon but it's not a comment"
pattern = "Oberon.*$"  Oberon Regex for matching comments

OberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberon
Oberon End of complex test file
OberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberonOberon