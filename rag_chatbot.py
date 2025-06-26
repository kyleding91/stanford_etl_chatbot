import os
from typing import List, Dict, Any, Optional
from openai import OpenAI
from dotenv import load_dotenv
from transcript_loader import TranscriptLoader
from vector_store import VectorStore

# Load environment variables
load_dotenv()

class RAGChatbot:
    """RAG chatbot for Stanford ETL transcripts."""
    
    def __init__(self, transcripts_dir: str, vector_store_dir: str = "./chroma_db"):
        """
        Initialize the RAG chatbot.
        
        Args:
            transcripts_dir: Directory containing transcript files
            vector_store_dir: Directory for vector store persistence
        """
        self.transcripts_dir = transcripts_dir
        self.vector_store = VectorStore(vector_store_dir)
        self.transcript_loader = TranscriptLoader(transcripts_dir)
        
        # Initialize OpenAI client
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        
        # System prompt for the chatbot
        self.system_prompt = """You are a helpful assistant that answers questions based on Stanford ETL (Entrepreneurship Through Leadership) transcripts. 

Your knowledge comes from hundreds of transcripts featuring successful entrepreneurs, investors, and business leaders sharing their insights, experiences, and advice.

When answering questions:
1. Use specific examples and quotes from the transcripts when relevant
2. Cite the source transcript title when referencing specific content
3. Provide practical, actionable advice based on the speakers' experiences
4. Be conversational but professional
5. If you don't have relevant information in the transcripts, say so rather than making things up

Always base your responses on the provided context from the transcripts."""
    
    def setup_vector_store(self, force_rebuild: bool = False) -> None:
        """
        Set up the vector store with transcript data.
        
        Args:
            force_rebuild: If True, clear existing data and rebuild
        """
        if force_rebuild:
            self.vector_store.clear_collection()
        
        # Check if vector store already has data
        collection_info = self.vector_store.get_collection_info()
        if collection_info["total_chunks"] > 0 and not force_rebuild:
            print(f"Vector store already contains {collection_info['total_chunks']} chunks")
            return
        
        # Load transcripts and add to vector store
        transcripts = self.transcript_loader.load_all_transcripts()
        if transcripts:
            self.vector_store.add_transcripts(transcripts)
        else:
            print("No transcripts found to add to vector store")
    
    def get_relevant_context(self, query: str, n_results: int = 5) -> str:
        """
        Get relevant context from vector store for a query.
        
        Args:
            query: User query
            n_results: Number of relevant chunks to retrieve
            
        Returns:
            Formatted context string
        """
        results = self.vector_store.search(query, n_results)
        
        if not results:
            return "No relevant context found."
        
        context_parts = []
        for i, result in enumerate(results, 1):
            content = result['content']
            metadata = result['metadata']
            title = metadata['title']
            
            context_parts.append(f"Source {i} (from '{title}'):\n{content}\n")
        
        return "\n".join(context_parts)
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate a response using OpenAI API.
        
        Args:
            query: User query
            context: Relevant context from transcripts
            
        Returns:
            Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Context from Stanford ETL transcripts:\n\n{context}\n\nQuestion: {query}\n\nPlease answer based on the provided context."}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat(self, query: str, n_context_results: int = 5) -> Dict[str, Any]:
        """
        Main chat method that processes a query and returns a response.
        
        Args:
            query: User query
            n_context_results: Number of context chunks to retrieve
            
        Returns:
            Dictionary containing response and metadata
        """
        # Get relevant context
        context = self.get_relevant_context(query, n_context_results)
        
        # Generate response
        response = self.generate_response(query, context)
        
        return {
            "query": query,
            "response": response,
            "context_used": context,
            "context_chunks": n_context_results
        }
    
    def get_transcript_summary(self) -> Dict[str, Any]:
        """
        Get summary of available transcripts.
        
        Returns:
            Dictionary with transcript statistics
        """
        return self.transcript_loader.get_transcript_summary()
    
    def get_vector_store_info(self) -> Dict[str, Any]:
        """
        Get information about the vector store.
        
        Returns:
            Dictionary with vector store statistics
        """
        return self.vector_store.get_collection_info()
    
    def search_transcripts(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search transcripts directly without generating a response.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of relevant chunks
        """
        return self.vector_store.search(query, n_results) 