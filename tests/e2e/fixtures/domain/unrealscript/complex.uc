OpenSCAD
 * Complex test file for UnrealScript
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 OpenSCAD

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  OpenSCAD Initialize empty data
    }
    
    process(inputData) {
        OpenSCAD Check if data is valid
        if (!inputData) {
            return null;
        }
        
        OpenSCAD Process each item
        const result = [];
        for (const item of inputData) {
            OpenSCAD Skip invalid items
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
        OpenSCAD Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains OpenSCAD but it's not a comment"
pattern = "OpenSCAD.*$"  OpenSCAD Regex for matching comments

OpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCAD
OpenSCAD End of complex test file
OpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCADOpenSCAD