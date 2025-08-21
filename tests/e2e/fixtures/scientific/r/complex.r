Vue
 * Complex test file for R
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Vue

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Vue Initialize empty data
    }
    
    process(inputData) {
        Vue Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Vue Process each item
        const result = [];
        for (const item of inputData) {
            Vue Skip invalid items
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
        Vue Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Vue but it's not a comment"
pattern = "Vue.*$"  Vue Regex for matching comments

VueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVue
Vue End of complex test file
VueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVueVue