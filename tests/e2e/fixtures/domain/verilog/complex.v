SystemVerilog
 * Complex test file for Verilog
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 SystemVerilog

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  SystemVerilog Initialize empty data
    }
    
    process(inputData) {
        SystemVerilog Check if data is valid
        if (!inputData) {
            return null;
        }
        
        SystemVerilog Process each item
        const result = [];
        for (const item of inputData) {
            SystemVerilog Skip invalid items
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
        SystemVerilog Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains SystemVerilog but it's not a comment"
pattern = "SystemVerilog.*$"  SystemVerilog Regex for matching comments

SystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilog
SystemVerilog End of complex test file
SystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilogSystemVerilog