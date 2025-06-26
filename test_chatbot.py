#!/usr/bin/env python3
"""
Test script for the Stanford ETL RAG Chatbot.
"""

import os
import sys
from rag_chatbot import RAGChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_chatbot():
    """Test the chatbot functionality."""
    print("🧪 Testing Stanford ETL RAG Chatbot")
    print("=" * 50)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment variables")
        return False
    
    # Initialize chatbot
    transcripts_dir = "/Users/xuehui/Library/Mobile Documents/com~apple~CloudDocs/Stanford ETL/Transcripts"
    
    if not os.path.exists(transcripts_dir):
        print(f"❌ Transcripts directory not found: {transcripts_dir}")
        return False
    
    try:
        chatbot = RAGChatbot(transcripts_dir)
        print("✅ Chatbot initialized successfully")
    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        return False
    
    # Test transcript loading
    print("\n📚 Testing transcript loading...")
    try:
        transcript_summary = chatbot.get_transcript_summary()
        print(f"✅ Loaded {transcript_summary.get('total_transcripts', 0)} transcripts")
        print(f"✅ Total words: {transcript_summary.get('total_words', 0):,}")
    except Exception as e:
        print(f"❌ Error loading transcripts: {str(e)}")
        return False
    
    # Test vector store
    print("\n🔍 Testing vector store...")
    try:
        vector_info = chatbot.get_vector_store_info()
        print(f"✅ Vector store contains {vector_info.get('total_chunks', 0)} chunks")
        
        if vector_info.get('total_chunks', 0) == 0:
            print("⚠️  Vector store is empty. Setting up...")
            chatbot.setup_vector_store()
            vector_info = chatbot.get_vector_store_info()
            print(f"✅ Vector store now contains {vector_info.get('total_chunks', 0)} chunks")
    except Exception as e:
        print(f"❌ Error with vector store: {str(e)}")
        return False
    
    # Test search functionality
    print("\n🔎 Testing search functionality...")
    try:
        test_query = "entrepreneurship advice"
        results = chatbot.search_transcripts(test_query, n_results=3)
        print(f"✅ Search returned {len(results)} results")
        
        if results:
            print("Sample result:")
            print(f"  Title: {results[0]['metadata']['title']}")
            print(f"  Content preview: {results[0]['content'][:100]}...")
    except Exception as e:
        print(f"❌ Error with search: {str(e)}")
        return False
    
    # Test chat functionality
    print("\n💬 Testing chat functionality...")
    try:
        test_question = "What advice do entrepreneurs give about starting a company?"
        print(f"Question: {test_question}")
        
        response = chatbot.chat(test_question, n_context_results=3)
        print(f"✅ Response generated successfully")
        print(f"Response preview: {response['response'][:200]}...")
        print(f"Context chunks used: {response['context_chunks']}")
    except Exception as e:
        print(f"❌ Error with chat: {str(e)}")
        return False
    
    print("\n🎉 All tests passed! The chatbot is working correctly.")
    return True

def main():
    """Main test function."""
    success = test_chatbot()
    
    if success:
        print("\n✅ Ready to use! You can now run:")
        print("  - streamlit run streamlit_app.py (for web interface)")
        print("  - python cli_chatbot.py (for command line interface)")
    else:
        print("\n❌ Tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 