import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from sentence_transformers import SentenceTransformer
import numpy as np

class VectorStore:
    """Handle vector storage and retrieval for the RAG system."""
    
    def __init__(self, persist_directory: str = "./chroma_db"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the vector database
        """
        self.persist_directory = persist_directory
        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Initialize embedding model
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Get or create collection
        self.collection = self.client.get_or_create_collection(
            name="stanford_etl_transcripts",
            metadata={"description": "Stanford ETL Transcripts Vector Database"}
        )
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to chunk
            chunk_size: Maximum size of each chunk
            overlap: Number of characters to overlap between chunks
            
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            
            # If this isn't the last chunk, try to break at a sentence boundary
            if end < len(text):
                # Look for sentence endings within the last 100 characters
                search_start = max(start, end - 100)
                for i in range(end, search_start, -1):
                    if text[i-1] in '.!?':
                        end = i
                        break
            
            chunk = text[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - overlap
            if start >= len(text):
                break
        
        return chunks
    
    def add_transcripts(self, transcripts: List[Dict[str, Any]]) -> None:
        """
        Add transcripts to the vector store.
        
        Args:
            transcripts: List of transcript dictionaries
        """
        print("Adding transcripts to vector store...")
        
        all_chunks = []
        all_metadatas = []
        all_ids = []
        
        for transcript in transcripts:
            title = transcript['title']
            content = transcript['content']
            
            # Chunk the content
            chunks = self.chunk_text(content)
            
            for i, chunk in enumerate(chunks):
                chunk_id = f"{title}_{i}"
                
                all_chunks.append(chunk)
                all_metadatas.append({
                    "title": title,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                    "word_count": len(chunk.split())
                })
                all_ids.append(chunk_id)
        
        # Add to collection in batches
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            batch_chunks = all_chunks[i:i+batch_size]
            batch_metadatas = all_metadatas[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            
            self.collection.add(
                documents=batch_chunks,
                metadatas=batch_metadatas,
                ids=batch_ids
            )
            
            print(f"Added batch {i//batch_size + 1}/{(len(all_chunks) + batch_size - 1)//batch_size}")
        
        print(f"Successfully added {len(all_chunks)} chunks to vector store")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for relevant chunks based on query.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of relevant chunks with metadata
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results['documents'][0])):
            formatted_results.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i]
            })
        
        return formatted_results
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the vector store collection.
        
        Returns:
            Dictionary with collection statistics
        """
        count = self.collection.count()
        
        return {
            "total_chunks": count,
            "collection_name": self.collection.name,
            "persist_directory": self.persist_directory
        }
    
    def clear_collection(self) -> None:
        """Clear all data from the collection."""
        self.client.delete_collection(name=self.collection.name)
        self.collection = self.client.create_collection(
            name="stanford_etl_transcripts",
            metadata={"description": "Stanford ETL Transcripts Vector Database"}
        )
        print("Collection cleared") 