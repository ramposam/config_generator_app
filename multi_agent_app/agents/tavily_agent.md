# Tavily Web Search Agent

## API Connection Details
- **Service**: Tavily AI Search API
- **Endpoint**: https://api.tavily.com
- **Authentication**: TAVILY_API_KEY (environment variable)
- **Search Depth**: basic (available: basic, advanced)
- **Max Results Per Query**: 5 results (default)

---

## Search Capabilities

### search_web Tool

**Purpose**: Search the web for information using Tavily's AI-powered search engine

**Supported Query Types**:
- General web searches
- News and current events
- Research topics
- Company/product information
- Technology trends
- Historical information
- Latest updates on any topic

**Parameters**:
- `query` (required, string): The search query to execute
  - Example: "latest AI trends 2024"
  - Example: "Python best practices"
  - Example: "COVID-19 vaccine updates"

**Return Format**:
```
Title: [Article/Page Title]
URL: [Source URL]
Content: [First 500 characters of content]...
---
[Next result...]
```

**Sample Response**:
```
Title: Latest AI Developments
URL: https://example.com/ai-news
Content: Artificial intelligence continues to evolve rapidly...
---
Title: Deep Learning Breakthrough
URL: https://example.com/deep-learning
Content: Researchers announce new breakthrough in neural networks...
```

---

## API Response Structure

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| results | array | Array of search results |
| results[].title | string | Title of the search result |
| results[].url | string | URL to the content |
| results[].content | string | Content snippet (truncated) |

---

## Search Best Practices

### Query Optimization
1. **Be Specific**: More specific queries return better results
   - ❌ "AI" 
   - ✅ "machine learning applications in healthcare 2024"

2. **Use Keywords**: Natural language queries work well
   - ❌ "information about"
   - ✅ "latest developments in quantum computing"

3. **Include Context**: Add relevant details to narrow results
   - ❌ "Python"
   - ✅ "Python data science libraries comparison"

4. **Current Events**: Great for time-sensitive information
   - ✅ "latest news today"
   - ✅ "recent tech company acquisitions"

### Result Usage
- **Max Results**: Each query returns up to 5 results
- **Content Length**: Content is truncated to 500 characters
- **Relevance**: Results are ranked by relevance
- **Freshness**: Results include recent sources

---

## Common Use Cases

### Research & Analysis
```
Query: "competitive analysis AI tools market 2024"
Use: Market research, competitor analysis
Returns: Recent articles and reports on AI tools
```

### News & Trending Topics
```
Query: "latest AI breakthroughs this month"
Use: Stay updated on industry trends
Returns: Recent news and announcements
```

### Technical Learning
```
Query: "Python async programming best practices"
Use: Learn new technologies and techniques
Returns: Tutorials, documentation, and examples
```

### Product Information
```
Query: "ChatGPT vs Claude vs Gemini comparison"
Use: Compare different products/services
Returns: Comparison articles and reviews
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| API Key Invalid | TAVILY_API_KEY not set | Set environment variable |
| Search Failed | Network issue or API down | Retry or check API status |
| No Results | Query too specific | Broaden the query terms |
| Rate Limited | Too many requests | Wait before retrying |

### Error Response Format
```
Error searching web: [specific error message]
```

---

## API Limitations

- **Rate Limiting**: Standard rate limits apply per API tier
- **Max Results**: 5 results per query
- **Content Truncation**: Results limited to 500 characters
- **Search Depth**: Basic depth for general searches
- **Response Time**: Typically 1-3 seconds

---

## Integration Notes

### With LLM Agent
The Tavily agent automatically:
1. Formats search queries for optimal results
2. Parses API responses into readable format
3. Handles errors gracefully
4. Returns structured information to the LLM

### Example Query Flow
```
User: "What are the latest developments in quantum computing?"
  ↓
Tavily Agent: Execute search_web("latest quantum computing developments")
  ↓
API Returns: 5 relevant articles with titles, URLs, and content
  ↓
LLM Processes: Analyzes results and provides summary to user
  ↓
User: Gets comprehensive answer with sources
```

---

## Performance Characteristics

| Metric | Value |
|--------|-------|
| Average Query Time | 1-3 seconds |
| Result Accuracy | High (AI-powered ranking) |
| Freshness | Current (crawled regularly) |
| Coverage | Global (multiple languages) |
| Reliability | 99%+ uptime |

---

## Sample Queries

### Technology
```
"latest machine learning breakthroughs"
"Python libraries for data science 2024"
"cloud computing trends"
```

### Business
```
"tech company acquisitions 2024"
"startup funding rounds"
"market analysis tech industry"
```

### Science
```
"recent medical research breakthroughs"
"climate change latest findings"
"space exploration updates"
```

### General
```
"today's news headlines"
"popular topics trending"
"how to [topic]"
```

---

## Tips for Best Results

1. **Use Natural Language**: Write queries like you would ask a person
2. **Add Context**: Include relevant details to narrow results
3. **Try Multiple Queries**: If first query doesn't work well, refine and retry
4. **Check URLs**: Verify source credibility from returned URLs
5. **Use Specific Terms**: More specific = better results

---

## Troubleshooting

### No Results Found
- Try different keywords
- Make query more general
- Check for typos in terms
- Use common alternative terms

### Irrelevant Results
- Add more specific criteria
- Include field/domain (e.g., "academic", "news")
- Use quotes for exact phrases: "exact phrase here"
- Exclude terms: use "NOT term" (if supported)

### API Connection Issues
- Verify TAVILY_API_KEY is set correctly
- Check internet connection
- Verify API service is online
- Check for rate limiting

---

## API Documentation References

- **Tavily API Docs**: https://tavily.com/api
- **Search Syntax**: Supports natural language queries
- **Rate Limits**: Varies by tier
- **Response Format**: JSON with search results


