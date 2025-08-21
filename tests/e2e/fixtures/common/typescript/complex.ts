C
 * Complex test file for TypeScript
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 C

import { Component } from 'framework';
import * as utils from './utils';

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  C Initialize empty data
    }
    
    process(inputData) {
        C Check if data is valid
        if (!inputData) {
            return null;
        }
        
        C Process each item
        const result = [];
        for (const item of inputData) {
            C Skip invalid items
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
        C Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains C but it's not a comment"
pattern = "C.*$"  C Regex for matching comments

CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC
C End of complex test file
CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC