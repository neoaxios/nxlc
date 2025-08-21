TeX
 * Complex test file for OpenSCAD
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 TeX

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  TeX Initialize empty data
    }
    
    process(inputData) {
        TeX Check if data is valid
        if (!inputData) {
            return null;
        }
        
        TeX Process each item
        const result = [];
        for (const item of inputData) {
            TeX Skip invalid items
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
        TeX Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains TeX but it's not a comment"
pattern = "TeX.*$"  TeX Regex for matching comments

TeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeX
TeX End of complex test file
TeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeXTeX