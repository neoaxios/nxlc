Assembly
 * Complex test file for JCL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Assembly

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Assembly Initialize empty data
    }
    
    process(inputData) {
        Assembly Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Assembly Process each item
        const result = [];
        for (const item of inputData) {
            Assembly Skip invalid items
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
        Assembly Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Assembly but it's not a comment"
pattern = "Assembly.*$"  Assembly Regex for matching comments

AssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssembly
Assembly End of complex test file
AssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssemblyAssembly