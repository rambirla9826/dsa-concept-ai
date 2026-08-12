import os
import json
import threading
from typing import Dict, List, Any, Optional
from datetime import datetime
from app.config import settings

class LocalJSONDatabase:
    """
    In-memory / JSON-backed document storage simulating Cloud Firestore structure.
    Enables local testing out-of-the-box without requiring initial GCP service credentials.
    """
    def __init__(self, data_file: str = "local_db.json"):
        self.data_file = data_file
        self._lock = threading.Lock()
        self.data: Dict[str, Dict[str, Any]] = {
            "users": {},
            "questions": {},
            "question_versions": {},
            "concept_blueprints": {},
            "rubrics": {},
            "submissions": {},
            "evaluations": {},
            "recommendations": {},
            "benchmarks": {},
            "ai_usage": {},
            "audit_logs": {}
        }
        self._load()

    def _load(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    for collection, docs in loaded.items():
                        self.data[collection] = docs
            except Exception as e:
                print(f"Error loading local DB: {e}")

    def _save(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, default=str)

    def get_document(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            col = self.data.get(collection, {})
            return col.get(doc_id)

    def set_document(self, collection: str, doc_id: str, data: Dict[str, Any]):
        with self._lock:
            if collection not in self.data:
                self.data[collection] = {}
            self.data[collection][doc_id] = data
            self._save()

    def update_document(self, collection: str, doc_id: str, updates: Dict[str, Any]):
        with self._lock:
            if collection in self.data and doc_id in self.data[collection]:
                self.data[collection][doc_id].update(updates)
                self._save()

    def delete_document(self, collection: str, doc_id: str):
        with self._lock:
            if collection in self.data and doc_id in self.data[collection]:
                del self.data[collection][doc_id]
                self._save()

    def list_collection(self, collection: str) -> List[Dict[str, Any]]:
        with self._lock:
            col = self.data.get(collection, {})
            return list(col.values())

    def query_collection(self, collection: str, field: str, value: Any) -> List[Dict[str, Any]]:
        with self._lock:
            col = self.data.get(collection, {})
            return [doc for doc in col.values() if doc.get(field) == value]

# Global DB instance
db = LocalJSONDatabase()
