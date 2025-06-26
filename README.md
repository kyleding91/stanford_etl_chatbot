# 🎓 Stanford ETL RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on Stanford ETL (Entrepreneurship Through Leadership) transcripts using OpenAI's GPT models.

## 🚀 Features

- **RAG-powered responses** based on 495+ Stanford ETL transcripts
- **Vector search** using ChromaDB and sentence transformers
- **Web interface** with Streamlit
- **Command-line interface** for quick queries
- **Production-ready** with Docker support
- **Multiple deployment options** (Streamlit Cloud, Docker, VPS)

## 📋 Prerequisites

- Python 3.8+
- OpenAI API key with sufficient quota
- Stanford ETL transcript files (495+ .txt files)

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/stanford-etl-chatbot.git
   cd stanford-etl-chatbot
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp env_example.txt .env
   # Edit .env with your OpenAI API key and transcripts directory
   ```

4. **Set up the vector database:**
   ```bash
   python setup_deployment.py
   ```

## 🎯 Usage

### Web Interface (Recommended)
```bash
streamlit run streamlit_app.py
```

### Command Line Interface
```bash
python cli_chatbot.py
```

### Test the System
```bash
python test_chatbot.py
```

## 📁 Project Structure

```
stanford-etl-chatbot/
├── rag_chatbot.py          # Main RAG chatbot logic
├── transcript_loader.py    # Transcript loading and processing
├── vector_store.py         # Vector database operations
├── streamlit_app.py        # Web interface
├── cli_chatbot.py          # Command-line interface
├── test_chatbot.py         # Test script
├── setup_deployment.py     # Deployment setup script
├── requirements.txt        # Python dependencies
├── Dockerfile              # Docker configuration
├── .streamlit/             # Streamlit configuration
├── deployment_guide.md     # Detailed deployment instructions
└── chroma_db/              # Vector database (generated, not in Git)
```

## 🌐 Deployment

### Quick Start: Streamlit Cloud
1. Push your code to GitHub (excluding `chroma_db/`)
2. Go to [Streamlit Cloud](https://share.streamlit.io/)
3. Connect your repository
4. Set main file: `streamlit_app.py`
5. Add environment variables in Streamlit Cloud settings

### Docker Deployment
```bash
# Build and run locally
docker build -t stanford-etl-chatbot .
docker run -p 8501:8501 -e OPENAI_API_KEY=your_key stanford-etl-chatbot

# Deploy to cloud providers (see deployment_guide.md)
```

### VPS/Server Deployment
See `deployment_guide.md` for detailed instructions on:
- DigitalOcean Droplet setup
- AWS EC2 configuration
- Nginx reverse proxy
- Systemd service management

## 🔧 Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key (required)
- `OPENAI_MODEL`: Model to use (default: `gpt-4o`)
- `TRANSCRIPTS_DIR`: Path to transcript files

### Vector Database
- The vector database (`chroma_db/`) is **not included in Git** due to size (231MB)
- It will be automatically generated when you run `setup_deployment.py`
- For deployment, the database will be rebuilt on the server

## 📊 Performance

- **495 transcripts** processed
- **23,300+ vector chunks** created
- **Fast semantic search** with ChromaDB
- **Context-aware responses** using RAG

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **"Vector store not found"**
   - Run `python setup_deployment.py` to create the vector database

2. **"OpenAI API quota exceeded"**
   - Check your OpenAI account billing and quota

3. **"Transcripts directory not found"**
   - Update the `TRANSCRIPTS_DIR` path in your `.env` file

4. **Large file size when pushing to GitHub**
   - The `chroma_db/` folder is excluded from Git
   - Run `git rm -r --cached chroma_db/` if already committed

### Getting Help

- Check the `deployment_guide.md` for detailed deployment instructions
- Review the test script output for system diagnostics
- Ensure all dependencies are installed correctly

## 🎯 Example Questions

- "What advice do successful entrepreneurs give about starting a company?"
- "How do venture capitalists evaluate startup investments?"
- "What are the key lessons from failed startups?"
- "How do successful founders build and lead teams?"
- "What role does innovation play in entrepreneurship?" 