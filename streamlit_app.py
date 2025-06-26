import streamlit as st
import os
from rag_chatbot import RAGChatbot
from dotenv import load_dotenv

# Streamlit Cloud Configuration
st.set_page_config(
    page_title="Stanford ETL Chatbot",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load environment variables
load_dotenv()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    .user-message {
        background-color: #f0f2f6;
        border-left-color: #1f77b4;
    }
    .assistant-message {
        background-color: #e8f4fd;
        border-left-color: #ff7f0e;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def initialize_chatbot():
    """Initialize the RAG chatbot."""
    # Use environment variable for transcripts directory, with fallback for local development
    transcripts_dir = os.getenv("TRANSCRIPTS_DIR", "./transcripts")
    
    if not os.path.exists(transcripts_dir):
        st.error(f"Transcripts directory not found: {transcripts_dir}")
        st.info("Please ensure the transcripts directory exists and contains .txt files")
        st.info("For deployment, set the TRANSCRIPTS_DIR environment variable")
        return None
    
    try:
        chatbot = RAGChatbot(transcripts_dir)
        return chatbot
    except Exception as e:
        st.error(f"Error initializing chatbot: {str(e)}")
        return None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 Stanford ETL Chatbot</h1>', unsafe_allow_html=True)
    st.markdown("Ask questions about entrepreneurship, leadership, and innovation based on Stanford ETL transcripts!")
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">Settings</div>', unsafe_allow_html=True)
        
        # Check API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("⚠️ OPENAI_API_KEY not found in environment variables")
            st.info("Please set your OpenAI API key in Streamlit Cloud secrets or .env file")
            st.markdown("""
            **For Streamlit Cloud:**
            1. Go to your app settings
            2. Add secrets with your OpenAI API key
            3. Redeploy the app
            """)
            return
        
        # Initialize chatbot
        chatbot = initialize_chatbot()
        if not chatbot:
            st.markdown("""
            **To fix this:**
            1. Upload your transcript files to the server
            2. Set the TRANSCRIPTS_DIR environment variable
            3. Or use the setup script: `python setup_deployment.py`
            """)
            return
        
        # Vector store setup
        st.markdown("### Vector Store")
        if st.button("Setup Vector Store"):
            with st.spinner("Setting up vector store..."):
                chatbot.setup_vector_store()
            st.success("Vector store setup complete!")
        
        if st.button("Rebuild Vector Store"):
            with st.spinner("Rebuilding vector store..."):
                chatbot.setup_vector_store(force_rebuild=True)
            st.success("Vector store rebuilt!")
        
        # Display info
        try:
            transcript_summary = chatbot.get_transcript_summary()
            vector_info = chatbot.get_vector_store_info()
            
            st.markdown("### Statistics")
            st.metric("Total Transcripts", transcript_summary.get("total_transcripts", 0))
            st.metric("Total Words", f"{transcript_summary.get('total_words', 0):,}")
            st.metric("Vector Chunks", vector_info.get("total_chunks", 0))
            
        except Exception as e:
            st.error(f"Error loading statistics: {str(e)}")
        
        # Context settings
        st.markdown("### Chat Settings")
        n_context_results = st.slider("Number of context chunks", 3, 10, 5)
        
        # Clear chat button
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()
    
    # Main chat interface
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask a question about entrepreneurship, leadership, or innovation..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    response = chatbot.chat(prompt, n_context_results)
                    
                    # Display response
                    st.markdown(response["response"])
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response["response"]})
                    
                    # Show context used (expandable)
                    with st.expander("View Context Used"):
                        st.text(response["context_used"])
                        
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
    
    # Example questions
    if not st.session_state.messages:
        st.markdown("### 💡 Example Questions")
        st.markdown("""
        - What advice do successful entrepreneurs give about starting a company?
        - How do venture capitalists evaluate startup investments?
        - What are the key lessons from failed startups?
        - How do successful founders build and lead teams?
        - What role does innovation play in entrepreneurship?
        - How do entrepreneurs handle failure and setbacks?
        - What are the most important qualities of a successful entrepreneur?
        - How do startups achieve product-market fit?
        """)

if __name__ == "__main__":
    main() 