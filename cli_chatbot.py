#!/usr/bin/env python3
"""
Command-line interface for the Stanford ETL RAG Chatbot.
"""

import os
import sys
from rag_chatbot import RAGChatbot
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_banner():
    """Print the application banner."""
    print("=" * 80)
    print("🎓 Stanford ETL Chatbot - Command Line Interface")
    print("Ask questions about entrepreneurship, leadership, and innovation!")
    print("=" * 80)
    print()

def print_help():
    """Print help information."""
    print("Available commands:")
    print("  /help     - Show this help message")
    print("  /stats    - Show transcript and vector store statistics")
    print("  /setup    - Setup the vector store with transcripts")
    print("  /rebuild  - Rebuild the vector store (clears existing data)")
    print("  /search   - Search transcripts without generating a response")
    print("  /quit     - Exit the application")
    print("  /clear    - Clear the screen")
    print()

def print_stats(chatbot):
    """Print statistics about the chatbot."""
    try:
        transcript_summary = chatbot.get_transcript_summary()
        vector_info = chatbot.get_vector_store_info()
        
        print("\n📊 Statistics:")
        print(f"  Total Transcripts: {transcript_summary.get('total_transcripts', 0)}")
        print(f"  Total Words: {transcript_summary.get('total_words', 0):,}")
        print(f"  Vector Chunks: {vector_info.get('total_chunks', 0)}")
        print(f"  Average Words per Transcript: {transcript_summary.get('average_words_per_transcript', 0):.0f}")
        print()
        
    except Exception as e:
        print(f"Error loading statistics: {str(e)}")

def search_transcripts(chatbot):
    """Interactive search function."""
    query = input("Enter search query: ").strip()
    if not query:
        return
    
    try:
        n_results = int(input("Number of results (default 5): ") or "5")
        results = chatbot.search_transcripts(query, n_results)
        
        print(f"\n🔍 Search Results for '{query}':")
        print("-" * 60)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Source: {result['metadata']['title']}")
            print(f"   Chunk {result['metadata']['chunk_index'] + 1}/{result['metadata']['total_chunks']}")
            print(f"   Distance: {result['distance']:.4f}")
            print(f"   Content: {result['content'][:200]}...")
        
        print()
        
    except ValueError:
        print("Invalid number of results. Using default of 5.")
    except Exception as e:
        print(f"Error searching: {str(e)}")

def main():
    """Main CLI function."""
    print_banner()
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OPENAI_API_KEY environment variable is required")
        print("Please set your OpenAI API key in a .env file")
        sys.exit(1)
    
    # Initialize chatbot
    transcripts_dir = "/Users/xuehui/Library/Mobile Documents/com~apple~CloudDocs/Stanford ETL/Transcripts"
    
    if not os.path.exists(transcripts_dir):
        print(f"❌ Error: Transcripts directory not found: {transcripts_dir}")
        sys.exit(1)
    
    try:
        chatbot = RAGChatbot(transcripts_dir)
        print("✅ Chatbot initialized successfully!")
        print()
    except Exception as e:
        print(f"❌ Error initializing chatbot: {str(e)}")
        sys.exit(1)
    
    # Show initial statistics
    print_stats(chatbot)
    
    # Main chat loop
    print("💬 Start chatting! Type /help for available commands.")
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            # Handle commands
            if user_input.startswith("/"):
                command = user_input.lower()
                
                if command == "/help":
                    print_help()
                elif command == "/stats":
                    print_stats(chatbot)
                elif command == "/setup":
                    print("🔄 Setting up vector store...")
                    chatbot.setup_vector_store()
                    print("✅ Vector store setup complete!")
                    print_stats(chatbot)
                elif command == "/rebuild":
                    confirm = input("⚠️  This will clear all existing data. Continue? (y/N): ")
                    if confirm.lower() == 'y':
                        print("🔄 Rebuilding vector store...")
                        chatbot.setup_vector_store(force_rebuild=True)
                        print("✅ Vector store rebuilt!")
                        print_stats(chatbot)
                    else:
                        print("Rebuild cancelled.")
                elif command == "/search":
                    search_transcripts(chatbot)
                elif command == "/quit":
                    print("👋 Goodbye!")
                    break
                elif command == "/clear":
                    os.system('clear' if os.name == 'posix' else 'cls')
                    print_banner()
                else:
                    print(f"❌ Unknown command: {user_input}")
                    print("Type /help for available commands.")
                
                continue
            
            # Generate response
            print("🤖 Thinking...")
            response = chatbot.chat(user_input)
            
            print(f"\n🤖 Assistant: {response['response']}")
            print()
            
            # Optionally show context
            show_context = input("Show context used? (y/N): ").strip().lower()
            if show_context == 'y':
                print("\n📚 Context Used:")
                print("-" * 60)
                print(response['context_used'])
                print("-" * 60)
                print()
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            print()

if __name__ == "__main__":
    main() 