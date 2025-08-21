Neo4j Cypher
 * Complex test file for CQL
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 Neo4j Cypher

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  Neo4j Cypher Initialize empty data
    }
    
    process(inputData) {
        Neo4j Cypher Check if data is valid
        if (!inputData) {
            return null;
        }
        
        Neo4j Cypher Process each item
        const result = [];
        for (const item of inputData) {
            Neo4j Cypher Skip invalid items
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
        Neo4j Cypher Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains Neo4j Cypher but it's not a comment"
pattern = "Neo4j Cypher.*$"  Neo4j Cypher Regex for matching comments

Neo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j Cypher
Neo4j Cypher End of complex test file
Neo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j CypherNeo4j Cypher