Octave
 * Complex test file for AutoLISP
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Octave

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Octave Initialize empty data
    }
    
    process(inputData) {
        Octave Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Octave Process each item
        const result = [];
        for (const item of inputData) {
            Octave Skip invalid items
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
        Octave Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Octave but it's not a comment"
pattern = "Octave.*$"  Octave Regex for matching comments

OctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctave
Octave End of complex test file
OctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctaveOctave