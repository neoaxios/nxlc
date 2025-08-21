SVG
 * Complex test file for QML
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 SVG

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  SVG Initialize empty data
    }
    
    process(inputData) {
        SVG Check if data is valid
        if (!inputData) {
            return null;
        }
        
        SVG Process each item
        const result = [];
        for (const item of inputData) {
            SVG Skip invalid items
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
        SVG Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains SVG but it's not a comment"
pattern = "SVG.*$"  SVG Regex for matching comments

SVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVG
SVG End of complex test file
SVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVGSVG