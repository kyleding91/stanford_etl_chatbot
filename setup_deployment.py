#!/usr/bin/env python3
"""
Setup script for Stanford ETL RAG Chatbot deployment.
This script helps set up the vector database on the server.
"""

import os
import sys
from rag_chatbot import RAGChatbot
from dotenv import load_dotenv

def main():
    """Main setup function."""
    print("🚀 Stanford ETL RAG Chatbot - Deployment Setup")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key in a .env file")
        sys.exit(1)
    
    # Get transcripts directory
    transcripts_dir = os.getenv("TRANSCRIPTS_DIR", "/app/transcripts")
    
    if not os.path.exists(transcripts_dir):
        print(f"❌ Error: Transcripts directory not found: {transcripts_dir}")
        print("Please ensure the transcripts directory exists and contains .txt files")
        sys.exit(1)
    
    # Initialize chatbot
    try:
        print("🔧 Initializing chatbot...")
        chatbot = RAGChatbot(transcripts_dir)
        print("✅ Chatbot initialized successfully!")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        sys.exit(1)
    
    # Check if vector store already exists
    vector_info = chatbot.get_vector_store_info()
    if vector_info.get("total_chunks", 0) > 0:
        print(f"✅ Vector store already contains {vector_info['total_chunks']} chunks")
        response = input("Do you want to rebuild the vector store? (y/N): ").strip().lower()
        if response != 'y':
            print("Setup complete! Vector store is ready.")
            return
    
    # Set up vector store
    print("🔄 Setting up vector store...")
    try:
        chatbot.setup_vector_store(force_rebuild=True)
        print("✅ Vector store setup complete!")
        
        # Show final statistics
        transcript_summary = chatbot.get_transcript_summary()
        vector_info = chatbot.get_vector_store_info()
        
        print("\n📊 Final Statistics:")
        print(f"  Total Transcripts: {transcript_summary.get('total_transcripts', 0)}")
        print(f"  Total Words: {transcript_summary.get('total_words', 0):,}")
        print(f"  Vector Chunks: {vector_info.get('total_chunks', 0)}")
        
        print("\n🎉 Setup complete! Your RAG chatbot is ready to use.")
        print("You can now run:")
        print("  - streamlit run streamlit_app.py (for web interface)")
        print("  - python cli_chatbot.py (for command line interface)")
        
    except Exception as e:
        print(f"❌ Error setting up vector store: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 