MediaWiki
 * Complex test file for ReStructuredText
 * 
 * This file tests:
 * - Nested comments (if supported)
 * - String literals with comment-like content
 * - Mixed code and comments
 * - Various comment styles
 MediaWiki

class DataProcessor {
    constructor(config) {
        this.config = config;
        this.data = [];  MediaWiki Initialize empty data
    }
    
    process(inputData) {
        MediaWiki Check if data is valid
        if (!inputData) {
            return null;
        }
        
        MediaWiki Process each item
        const result = [];
        for (const item of inputData) {
            MediaWiki Skip invalid items
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
        MediaWiki Apply transformation
        return typeof item === 'string' ? item.toUpperCase() : item;
    }
}

message = "This string contains MediaWiki but it's not a comment"
pattern = "MediaWiki.*$"  MediaWiki Regex for matching comments

MediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWiki
MediaWiki End of complex test file
MediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWikiMediaWiki