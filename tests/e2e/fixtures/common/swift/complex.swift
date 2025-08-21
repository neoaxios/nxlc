Shell
 * Complex test file for Swift
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Shell

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Shell Initialize empty data
    }
    
    process(inputData) {
        Shell Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Shell Process each item
        const result = [];
        for (const item of inputData) {
            Shell Skip invalid items
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
        Shell Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Shell but it's not a comment"
pattern = "Shell.*$"  Shell Regex for matching comments

ShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShell
Shell End of complex test file
ShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShellShell