Mathematica
 * Complex test file for TCL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Mathematica

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Mathematica Initialize empty data
    }
    
    process(inputData) {
        Mathematica Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Mathematica Process each item
        const result = [];
        for (const item of inputData) {
            Mathematica Skip invalid items
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
        Mathematica Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Mathematica but it's not a comment"
pattern = "Mathematica.*$"  Mathematica Regex for matching comments

MathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematica
Mathematica End of complex test file
MathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematicaMathematica