RPG
 * Complex test file for ALGOL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 RPG

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  RPG Initialize empty data
    }
    
    process(inputData) {
        RPG Check if data is valid
        if (!inputData) {
            return null;
        }
        
        RPG Process each item
        const result = [];
        for (const item of inputData) {
            RPG Skip invalid items
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
        RPG Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains RPG but it's not a comment"
pattern = "RPG.*$"  RPG Regex for matching comments

RPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPG
RPG End of complex test file
RPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPGRPG