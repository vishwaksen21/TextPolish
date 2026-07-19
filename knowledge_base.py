"""
Avelyn — Local Knowledge Base (RAG)
==================================
Handles importing documents (TXT, MD, PDF, DOCX), chunking them,
indexing them locally, and performing local TF-IDF semantic searches.
No cloud APIs, 100% private and offline.
"""

import os
import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

from logger import logger

KNOWLEDGE_DIR = Path.home() / ".avelyn" / "knowledge"
INDEX_FILE = KNOWLEDGE_DIR / "index.json"

class KnowledgeBaseManager:
    """Manages local documents and slices them into search retrieve context blocks."""

    def __init__(self) -> None:
        KNOWLEDGE_DIR.mkdir(parents=True, exist_ok=True)
        self.documents: List[Dict[str, Any]] = []
        self.load_index()

    def load_index(self) -> None:
        if INDEX_FILE.exists():
            try:
                with open(INDEX_FILE, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
            except Exception as e:
                logger.error("Failed to load knowledge base index: %s", e)
                self.documents = []
        else:
            self.documents = []
            self.save_index()

    def save_index(self) -> None:
        try:
            with open(INDEX_FILE, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, indent=2, ensure_ascii=False)
        except Exception as e:
            logger.error("Failed to save knowledge base index: %s", e)

    def import_document(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = path.suffix.lower()
        text = ""

        # Extract text based on file format
        if ext in (".txt", ".text"):
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif ext == ".md":
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()
        elif ext == ".pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(path)
                pages_text = []
                for p in reader.pages:
                    t = p.extract_text()
                    if t:
                        pages_text.append(t)
                text = "\n".join(pages_text)
            except ImportError:
                raise ImportError("pypdf package is not installed.")
        elif ext == ".docx":
            try:
                import docx
                doc = docx.Document(path)
                paragraphs = [p.text for p in doc.paragraphs]
                text = "\n".join(paragraphs)
            except ImportError:
                raise ImportError("python-docx package is not installed.")
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        text_cleaned = text.strip()
        if not text_cleaned:
            raise ValueError("Extracted text from document is empty.")

        # Chunk the text into search paragraphs (overlapping word sequences)
        chunks = self._chunk_text(text_cleaned)

        doc_item = {
            "id": str(uuid.uuid4()),
            "title": path.name,
            "filename": path.name,
            "path": str(path.absolute()),
            "text": text_cleaned,
            "chunks": chunks,
            "imported_at": datetime.now().isoformat()
        }

        # Keep only one instance of the same filename in the library
        self.documents = [d for d in self.documents if d["filename"] != path.name]
        self.documents.append(doc_item)
        self.save_index()
        logger.info("Imported document: %s (%d chunks)", path.name, len(chunks))
        return doc_item

    def delete_document(self, doc_id: str) -> bool:
        initial_count = len(self.documents)
        self.documents = [d for d in self.documents if d["id"] != doc_id]
        if len(self.documents) < initial_count:
            self.save_index()
            logger.info("Deleted document with ID: %s", doc_id)
            return True
        return False

    def _chunk_text(self, text: str, chunk_size: int = 150, overlap: int = 30) -> List[str]:
        words = text.split()
        if not words:
            return []
        
        chunks = []
        step = chunk_size - overlap
        if step <= 0:
            step = chunk_size

        for i in range(0, len(words), step):
            chunk_words = words[i:i + chunk_size]
            chunk = " ".join(chunk_words)
            if chunk.strip():
                chunks.append(chunk)
        return chunks

    def search_context(self, query: str, top_k: int = 3) -> str:
        """
        Query local TF-IDF semantic indexes to locate relevant context paragraphs.
        """
        if not self.documents:
            return ""

        # Collect all chunks with their source document tags
        all_chunks: List[str] = []
        chunk_sources: List[str] = []

        for doc in self.documents:
            for c in doc.get("chunks", []):
                all_chunks.append(c)
                chunk_sources.append(doc["title"])

        if not all_chunks:
            return ""

        try:
            from sklearn.feature_extraction.text import TfidfVectorizer
            from sklearn.metrics.pairwise import cosine_similarity
            import numpy as np

            # Build local TF-IDF matrix
            vectorizer = TfidfVectorizer(stop_words='english')
            tfidf_matrix = vectorizer.fit_transform(all_chunks)
            query_vector = vectorizer.transform([query])

            # Compute similarities
            similarities = cosine_similarity(query_vector, tfidf_matrix).flatten()
            
            # Sort and select top_k
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            retrieved = []
            for idx in top_indices:
                if similarities[idx] > 0.05:  # threshold to prevent noise
                    retrieved.append(f"[{chunk_sources[idx]}]: {all_chunks[idx]}")

            if retrieved:
                return "\n\n".join(retrieved)
        except Exception as e:
            logger.error("TF-IDF retrieval error: %s", e)
            # Fallback to simple keyword overlap search
            q_words = set(query.lower().split())
            scores = []
            for c in all_chunks:
                c_words = set(c.lower().split())
                overlap = len(q_words.intersection(c_words))
                scores.append(overlap)
            
            import numpy as np
            top_indices = np.argsort(scores)[::-1][:top_k]
            retrieved = []
            for idx in top_indices:
                if scores[idx] > 0:
                    retrieved.append(f"[{chunk_sources[idx]}]: {all_chunks[idx]}")
            return "\n\n".join(retrieved)

        return ""

    def get_context_for_prompt(self, prompt: str) -> str:
        """
        Scan user prompt for reference keywords (e.g. 'resume', 'guidelines') matching
        imported document titles, and pull semantic context.
        """
        if not self.documents:
            return ""

        prompt_lower = prompt.lower()
        matched_titles = []
        
        for doc in self.documents:
            # Clean filename to get a nice keyword tag
            name_clean = Path(doc["filename"]).stem.lower()
            # If doc title/name is mentioned in the prompt
            if name_clean in prompt_lower or doc["title"].lower() in prompt_lower:
                matched_titles.append(doc["title"])

        # Also support general lookup words if specifically asked
        kb_keywords = ["resume", "guidelines", "notes", "knowledge", "reference"]
        has_general_trigger = any(kw in prompt_lower for kw in kb_keywords)

        if not matched_titles and not has_general_trigger:
            return ""

        # Perform semantic query search in matching documents/chunks
        context = self.search_context(prompt, top_k=4)
        if context:
            return (
                "--- LOCAL KNOWLEDGE BASE CONTEXT ---\n"
                f"You have access to the following relevant sections from imported documents:\n\n"
                f"{context}\n"
                "------------------------------------\n"
            )
        return ""
