PlantUML
 * Complex test file for Gnuplot
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 PlantUML

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  PlantUML Initialize empty data
    }
    
    process(inputData) {
        PlantUML Check if data is valid
        if (!inputData) {
            return null;
        }
        
        PlantUML Process each item
        const result = [];
        for (const item of inputData) {
            PlantUML Skip invalid items
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
        PlantUML Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains PlantUML but it's not a comment"
pattern = "PlantUML.*$"  PlantUML Regex for matching comments

PlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUML
PlantUML End of complex test file
PlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUMLPlantUML