import os
import glob
from typing import List, Dict, Any
from pathlib import Path

class TranscriptLoader:
    """Load and process transcript files from the Stanford ETL directory."""
    
    def __init__(self, transcripts_dir: str):
        """
        Initialize the transcript loader.
        
        Args:
            transcripts_dir: Path to the directory containing transcript files
        """
        self.transcripts_dir = Path(transcripts_dir)
        
    def get_transcript_files(self) -> List[str]:
        """Get all .txt files in the transcripts directory."""
        pattern = self.transcripts_dir / "*.txt"
        return glob.glob(str(pattern))
    
    def load_transcript(self, file_path: str) -> Dict[str, Any]:
        """
        Load a single transcript file and extract metadata.
        
        Args:
            file_path: Path to the transcript file
            
        Returns:
            Dictionary containing transcript content and metadata
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            # Extract filename as title
            filename = Path(file_path).stem
            
            return {
                'title': filename,
                'content': content,
                'file_path': file_path,
                'file_size': len(content),
                'word_count': len(content.split())
            }
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            return None
    
    def load_all_transcripts(self) -> List[Dict[str, Any]]:
        """
        Load all transcript files from the directory.
        
        Returns:
            List of transcript dictionaries
        """
        transcript_files = self.get_transcript_files()
        transcripts = []
        
        print(f"Found {len(transcript_files)} transcript files")
        
        for file_path in transcript_files:
            transcript = self.load_transcript(file_path)
            if transcript:
                transcripts.append(transcript)
                print(f"Loaded: {transcript['title']} ({transcript['word_count']} words)")
        
        print(f"Successfully loaded {len(transcripts)} transcripts")
        return transcripts
    
    def get_transcript_summary(self) -> Dict[str, Any]:
        """
        Get a summary of all loaded transcripts.
        
        Returns:
            Dictionary with summary statistics
        """
        transcripts = self.load_all_transcripts()
        
        if not transcripts:
            return {"error": "No transcripts found"}
        
        total_words = sum(t['word_count'] for t in transcripts)
        total_size = sum(t['file_size'] for t in transcripts)
        
        return {
            "total_transcripts": len(transcripts),
            "total_words": total_words,
            "total_size": total_size,
            "average_words_per_transcript": total_words / len(transcripts),
            "transcript_titles": [t['title'] for t in transcripts]
        } 