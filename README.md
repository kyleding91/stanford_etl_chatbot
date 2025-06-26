# 🎓 Stanford ETL RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions about entrepreneurship, leadership, and innovation based on Stanford ETL (Entrepreneurship Through Leadership) transcripts.

## Features

- **RAG-powered responses**: Uses vector search to find relevant transcript content and generates contextual responses
- **Comprehensive knowledge base**: Access to hundreds of Stanford ETL transcripts featuring successful entrepreneurs, investors, and business leaders
- **Multiple interfaces**: Web interface (Streamlit) and command-line interface
- **Smart text chunking**: Intelligent document segmentation for better retrieval
- **Persistent vector store**: Uses ChromaDB for efficient storage and retrieval
- **Source attribution**: Cites specific transcript sources in responses

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Access to Stanford ETL transcripts directory

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd stanford_etl_chatbot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```bash
   cp env_example.txt .env
   ```
   
   Edit the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Web Interface (Recommended)

1. **Start the Streamlit app**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open your browser** and navigate to the provided URL (usually `http://localhost:8501`)

3. **Setup the vector store**:
   - Click "Setup Vector Store" in the sidebar to process your transcripts
   - Wait for the setup to complete

4. **Start chatting**:
   - Ask questions about entrepreneurship, leadership, or innovation
   - View the context used for each response by expanding "View Context Used"

### Command Line Interface

1. **Run the CLI chatbot**:
   ```bash
   python cli_chatbot.py
   ```

2. **Available commands**:
   - `/help` - Show help information
   - `/stats` - Show transcript and vector store statistics
   - `/setup` - Setup the vector store with transcripts
   - `/rebuild` - Rebuild the vector store (clears existing data)
   - `/search` - Search transcripts without generating a response
   - `/quit` - Exit the application
   - `/clear` - Clear the screen

3. **Start chatting**:
   - Type your questions directly
   - Choose whether to view the context used for each response

## Example Questions

Here are some example questions you can ask:

- What advice do successful entrepreneurs give about starting a company?
- How do venture capitalists evaluate startup investments?
- What are the key lessons from failed startups?
- How do successful founders build and lead teams?
- What role does innovation play in entrepreneurship?
- How do entrepreneurs handle failure and setbacks?
- What are the most important qualities of a successful entrepreneur?
- How do startups achieve product-market fit?
- What are the biggest challenges in scaling a startup?
- How do successful entrepreneurs balance work and life?

## Project Structure

```
stanford_etl_chatbot/
├── transcript_loader.py      # Load and process transcript files
├── vector_store.py          # Vector storage and retrieval with ChromaDB
├── rag_chatbot.py           # Main RAG chatbot implementation
├── streamlit_app.py         # Web interface using Streamlit
├── cli_chatbot.py           # Command-line interface
├── requirements.txt         # Python dependencies
├── env_example.txt          # Example environment variables
└── README.md               # This file
```

## How It Works

1. **Document Processing**: Transcript files are loaded and chunked into smaller, overlapping segments
2. **Vector Embedding**: Each chunk is converted into a vector representation using sentence transformers
3. **Storage**: Vectors are stored in ChromaDB for efficient retrieval
4. **Retrieval**: When a question is asked, the system finds the most relevant chunks using vector similarity
5. **Generation**: The relevant context is sent to OpenAI's API along with the question to generate a response
6. **Response**: The system returns an answer based on the transcript content

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: OpenAI model to use (default: `gpt-4-turbo-preview`)
- `EMBEDDING_MODEL`: Embedding model for vector creation (default: `text-embedding-ada-002`)

### Customization

You can customize various aspects of the chatbot:

- **Chunk size**: Modify the `chunk_size` parameter in `vector_store.py`
- **Number of context chunks**: Adjust the `n_context_results` parameter
- **System prompt**: Edit the `system_prompt` in `rag_chatbot.py`
- **Model parameters**: Change temperature, max tokens, etc. in the OpenAI API calls

## Troubleshooting

### Common Issues

1. **"OPENAI_API_KEY not found"**:
   - Make sure you've created a `.env` file with your API key
   - Verify the API key is valid and has sufficient credits

2. **"Transcripts directory not found"**:
   - Update the `transcripts_dir` path in the code to match your setup
   - Ensure the directory contains `.txt` files

3. **Vector store setup fails**:
   - Check that all transcript files are readable
   - Ensure sufficient disk space for the vector database
   - Try rebuilding the vector store with `/rebuild` command

4. **Slow responses**:
   - Reduce the number of context chunks retrieved
   - Use a faster OpenAI model (e.g., `gpt-3.5-turbo`)
   - Consider upgrading your OpenAI API plan

### Performance Tips

- The first run will be slower as it processes all transcripts
- Subsequent runs will be faster as the vector store is already built
- Use the CLI for faster interaction if you prefer terminal-based interfaces
- Adjust chunk size and overlap for optimal performance vs. accuracy trade-off

## Contributing

Feel free to contribute to this project by:

1. Reporting bugs or issues
2. Suggesting new features
3. Improving documentation
4. Optimizing performance
5. Adding new transcript sources

## License

This project is for educational purposes. Please respect the intellectual property of the Stanford ETL transcripts.

## Acknowledgments

- Stanford ETL for providing the valuable transcript content
- OpenAI for the GPT models and API
- ChromaDB for vector storage
- Streamlit for the web interface framework
- The open-source community for the various libraries used 