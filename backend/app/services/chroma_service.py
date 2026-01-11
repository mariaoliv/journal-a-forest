"""
Chroma Vector Database Service for semantic search and retrieval.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Optional
import chromadb
import json
from chromadb.config import Settings
from mistralai import Mistral

load_dotenv()
MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY")
CHROMA_DB_PATH = Path("chroma_db")

class ChromaService:
    """
    Service for managing Chroma vector database.
    
    1. Initialize persistent Chroma client
    2. Create collection for journal entries
    3. Generate embeddings (using OpenAI or sentence-transformers)
    4. Store entry text with metadata (session_id, entry_id, timestamp)
    5. Query for similar entries
    6. Retrieve context for LLM prompts
    """
    
    def __init__(self):
        self.initialized = False
        self.client = chromadb.PersistentClient(
            path=str(CHROMA_DB_PATH),
            settings=Settings(anonymized_telemetry=False)
        )
        self.collection = self.client.get_or_create_collection(
            name="journal_entries",
            metadata={"hnsw:space": "cosine"}
        )
        self.mistral_client = Mistral(api_key=MISTRAL_API_KEY)
        self.initialized = True
    
    def store_entry(self, entry_id: int, session_id: str, text: str, metadata: Dict = None):
        """
        Store entry text as embedding in Chroma.
        
        The texts will be short summaries of journal entries, so chunking is not needed.
        """
        if not self.initialized:
            return

        try:
            metadata["session_id"] = session_id

            for k, v in metadata.items():
                if type(v) == list or type(v) == dict:
                    metadata[k] = json.dumps(v)

            embedding = self._generate_embedding(text)
            self.collection.add(
                ids=[f"{session_id}_{entry_id}"],
                embeddings=[embedding],
                documents=text,
                metadatas=metadata
            )
        except Exception as e:
            print(f"Could not store entry in ChromaDB: {e}")

    
    def search_similar(self, query: str, session_id: str, exclude_entry_ids: List[str] = [], limit: int = 5) -> List[Dict]:
        """
        Search for similar entries using semantic similarity.
        """
        if not self.initialized:
            return []
        
        try:
            query_embedding = self._generate_embedding(query)
            if not exclude_entry_ids:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where={"session_id" : session_id}
                )
            else:
                results = self.collection.query(
                    query_embeddings=[query_embedding],
                    n_results=limit,
                    where={
                        "$and" : [
                            {"session_id": session_id},
                            {"entry_id": {"$nin": exclude_entry_ids}}
                        ]
                    }
                   
                )
            return results["documents"][0] if results["documents"] else []
        except Exception as e:
            print(f"Failed to perform similarity search: {e}")
    
    def delete_session_entries(self, session_id: str):
        """
        Delete all entries for a session from Chroma.
        """
        if not self.initialized:
            return
        
        try:
            results = self.collection.get(where={"session_id" : session_id})
            if results and results["ids"]:
                self.collection.delete(ids=results["ids"])
        except Exception as e:
            print(f"Failed to delete session entries: {e}")
    
    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text.
        """
        try:
            response = self.mistral_client.embeddings.create(
                model="mistral-embed",
                inputs=text
            )
            return response.data[0].embedding
        except Exception as e:
            print(f"Failed to generate embedding: {e}")

# Global instance
chroma_service = ChromaService()

