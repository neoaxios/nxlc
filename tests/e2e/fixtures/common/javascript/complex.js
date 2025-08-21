Java
 * Complex test file for JavaScript
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Java

import { Component } from 'framework';
import * as utils from './utils';

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Java Initialize empty data
    }
    
    process(inputData) {
        Java Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Java Process each item
        const result = [];
        for (const item of inputData) {
            Java Skip invalid items
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
        Java Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Java but it's not a comment"
pattern = "Java.*$"  Java Regex for matching comments

JavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJava
Java End of complex test file
JavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJavaJava