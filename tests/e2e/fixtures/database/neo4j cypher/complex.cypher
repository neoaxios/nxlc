Verilog
 * Complex test file for Neo4j Cypher
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Verilog

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Verilog Initialize empty data
    }
    
    process(inputData) {
        Verilog Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Verilog Process each item
        const result = [];
        for (const item of inputData) {
            Verilog Skip invalid items
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
        Verilog Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Verilog but it's not a comment"
pattern = "Verilog.*$"  Verilog Regex for matching comments

VerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilog
Verilog End of complex test file
VerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilogVerilog