import os
import json
import pickle
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class SimpleVectorStore:
    """Simple vector store using sentence transformers and numpy."""
    
    def __init__(self, store_dir: str = "./simple_vector_store"):
        """
        Initialize the simple vector store.
        
        Args:
            store_dir: Directory for storing vectors and metadata
        """
        self.store_dir = store_dir
        self.embeddings_file = os.path.join(store_dir, "embeddings.pkl")
        self.metadata_file = os.path.join(store_dir, "metadata.json")
        
        # Create directory if it doesn't exist
        os.makedirs(store_dir, exist_ok=True)
        
        # Initialize sentence transformer model
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Load existing data if available
        self.embeddings = []
        self.metadata = []
        self._load_data()
    
    def _load_data(self):
        """Load existing embeddings and metadata."""
        if os.path.exists(self.embeddings_file) and os.path.exists(self.metadata_file):
            try:
                with open(self.embeddings_file, 'rb') as f:
                    self.embeddings = pickle.load(f)
                with open(self.metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                print(f"Loaded {len(self.embeddings)} existing embeddings")
            except Exception as e:
                print(f"Error loading existing data: {e}")
                self.embeddings = []
                self.metadata = []
    
    def _save_data(self):
        """Save embeddings and metadata to disk."""
        try:
            with open(self.embeddings_file, 'wb') as f:
                pickle.dump(self.embeddings, f)
            with open(self.metadata_file, 'w') as f:
                json.dump(self.metadata, f)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]] = None):
        """
        Add texts to the vector store.
        
        Args:
            texts: List of text chunks
            metadatas: List of metadata dictionaries
        """
        if not texts:
            return
        
        # Generate embeddings
        print(f"Generating embeddings for {len(texts)} texts...")
        new_embeddings = self.model.encode(texts, show_progress_bar=True)
        
        # Add to existing data
        self.embeddings.extend(new_embeddings)
        if metadatas:
            self.metadata.extend(metadatas)
        else:
            self.metadata.extend([{"index": i} for i in range(len(texts))])
        
        # Save to disk
        self._save_data()
        print(f"Added {len(texts)} texts to vector store")
    
    def search(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """
        Search for similar texts.
        
        Args:
            query: Search query
            n_results: Number of results to return
            
        Returns:
            List of dictionaries with 'content' and 'metadata' keys
        """
        if not self.embeddings:
            return []
        
        # Encode query
        query_embedding = self.model.encode([query])
        
        # Calculate similarities
        similarities = cosine_similarity(query_embedding, self.embeddings)[0]
        
        # Get top results
        top_indices = np.argsort(similarities)[::-1][:n_results]
        
        results = []
        for idx in top_indices:
            results.append({
                'content': self.metadata[idx].get('content', ''),
                'metadata': {k: v for k, v in self.metadata[idx].items() if k != 'content'},
                'similarity': float(similarities[idx])
            })
        
        return results
    
    def clear_collection(self):
        """Clear all data from the vector store."""
        self.embeddings = []
        self.metadata = []
        if os.path.exists(self.embeddings_file):
            os.remove(self.embeddings_file)
        if os.path.exists(self.metadata_file):
            os.remove(self.metadata_file)
        print("Vector store cleared")
    
    def get_collection_info(self) -> Dict[str, Any]:
        """Get information about the vector store."""
        return {
            "total_chunks": len(self.embeddings),
            "embedding_dimension": self.embeddings[0].shape[0] if self.embeddings else 0,
            "store_directory": self.store_dir
        } 