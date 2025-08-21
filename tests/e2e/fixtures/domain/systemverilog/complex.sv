AutoLISP
 * Complex test file for SystemVerilog
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 AutoLISP

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  AutoLISP Initialize empty data
    }
    
    process(inputData) {
        AutoLISP Check if data is valid
        if (!inputData) {
            return null;
        }
        
        AutoLISP Process each item
        const result = [];
        for (const item of inputData) {
            AutoLISP Skip invalid items
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
        AutoLISP Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains AutoLISP but it's not a comment"
pattern = "AutoLISP.*$"  AutoLISP Regex for matching comments

AutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISP
AutoLISP End of complex test file
AutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISPAutoLISP