# Qdrant Schema Documentation

## Collection: textbook_chunks

### Overview
The `textbook_chunks` collection stores embedded chunks of the Physical AI & Humanoid Robotics textbook with semantic search capabilities.

### Embedding Model
- **Model**: (To be specified based on actual implementation)
- **Dimensions**: (To be specified)
- **Distance Metric**: Cosine similarity

### Payload Schema

Each vector in the collection includes the following metadata in its payload:

```json
{
  "text": "string",          // The actual textbook content chunk
  "chapter": "string",       // Chapter number (e.g., "1", "2", "3")
  "section": "string",       // Section identifier (e.g., "1.1", "2.3")
  "page": "string",          // Page number or reference
  "content_type": "string"   // Type of content: "text", "code", or "diagram"
}
```

### Content Types

The `content_type` field categorizes chunks into three types:

#### 1. Text (`"text"`)
- Standard textbook paragraphs and explanations
- Conceptual descriptions
- Theoretical content
- Default type for most chunks

**Example**:
```json
{
  "text": "ROS 2 (Robot Operating System 2) is a flexible framework for writing robot software...",
  "chapter": "1",
  "section": "1.2",
  "page": "5",
  "content_type": "text"
}
```

#### 2. Code (`"code"`)
- Programming examples
- Code snippets
- Configuration files
- Terminal commands

**Example**:
```json
{
  "text": "import rclpy\nfrom rclpy.node import Node\n\nclass MinimalPublisher(Node):...",
  "chapter": "1",
  "section": "1.4",
  "page": "12",
  "content_type": "code"
}
```

#### 3. Diagram (`"diagram"`)
- Figures and illustrations
- Architecture diagrams
- Flowcharts
- Visual representations

**Example**:
```json
{
  "text": "Figure 2.1: ROS 2 Communication Architecture - Shows the publisher-subscriber pattern...",
  "chapter": "2",
  "section": "2.1",
  "page": "18",
  "content_type": "diagram"
}
```

### Filtering by Content Type

The Qdrant service supports filtering searches by content type:

```python
# Search for only code examples
results = await qdrant_service.search(
    query="How to create a ROS 2 publisher?",
    filters={"content_type": "code"}
)

# Search for only diagrams
results = await qdrant_service.search(
    query="Show me the ROS 2 architecture",
    filters={"content_type": "diagram"}
)
```

### Search Results Format

Search results from the Qdrant service include content type in metadata:

```python
{
    "content": "The actual chunk text...",
    "metadata": {
        "chapter": "1",
        "section": "1.2",
        "page": "5",
        "content_type": "text"  # Available for all chunks
    },
    "score": 0.85
}
```

### Implementation Notes

1. **Content Type Detection**: Content type is determined during the embedding pipeline and stored in Qdrant metadata.

2. **Default Value**: If `content_type` is not specified in the payload, the Qdrant service defaults to `"text"` for backward compatibility.

3. **Case Sensitivity**: Content types are lowercase strings: `"text"`, `"code"`, `"diagram"`.

4. **Extensibility**: Additional content types can be added in the future (e.g., `"table"`, `"equation"`) without breaking existing code.

### Multi-Modal Search Strategy

When handling questions that may require different content types:

1. **Initial Search**: Retrieve chunks without filtering by content type
2. **Content Analysis**: Examine the `content_type` distribution in results
3. **Adaptive Prompting**: Adjust Gemini prompts based on content types present
4. **Citation Enhancement**: Display appropriate icons/labels based on content type

### Verification Checklist

- ✅ Qdrant service extracts `content_type` from payload
- ✅ Default value `"text"` applied when not present
- ✅ Metadata accessible in search results
- ✅ Filtering by content type supported
- ✅ Documentation complete

### Future Enhancements

1. **Content Type Statistics**: Track content type distribution across chapters
2. **Type-Specific Ranking**: Boost certain content types based on query intent
3. **Visual Content Links**: Store direct URLs to diagram images
4. **Code Syntax Metadata**: Add language information for code chunks (e.g., `language: "python"`)
