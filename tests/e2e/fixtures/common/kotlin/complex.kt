PowerShell
 * Complex test file for Kotlin
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 PowerShell

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  PowerShell Initialize empty data
    }
    
    process(inputData) {
        PowerShell Check if data is valid
        if (!inputData) {
            return null;
        }
        
        PowerShell Process each item
        const result = [];
        for (const item of inputData) {
            PowerShell Skip invalid items
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
        PowerShell Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains PowerShell but it's not a comment"
pattern = "PowerShell.*$"  PowerShell Regex for matching comments

PowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShell
PowerShell End of complex test file
PowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShellPowerShell