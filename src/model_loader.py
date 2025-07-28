"""
Lightweight Model Loader - No Heavy Dependencies
"""

import os
import pickle
import spacy
import numpy as np
import re
from pathlib import Path
from flashrank import Ranker
from collections import Counter
from typing import List, Dict, Any

class OfflineModelLoader:
    def __init__(self):
        self.project_root = Path("/app")
        self.models_dir = self.project_root / "models"
        self.setup_offline_environment()
        
    def setup_offline_environment(self):
        """Configure environment for offline execution"""
        os.environ['HF_HUB_OFFLINE'] = '1'
        os.environ['FLASHRANK_CACHE_DIR'] = str(self.models_dir / "flashrank")
        
    def load_spacy_model(self):
        """Load spaCy model"""
        try:
            local_model_path = str(self.models_dir / "spacy" / "en_core_web_sm")
            return spacy.load(local_model_path)
        except:
            return spacy.load("en_core_web_sm")
    
    def load_flashrank_model(self):
        """Load FlashRank model"""
        cache_dir = str(self.models_dir / "flashrank")
        return Ranker(model_name="ms-marco-MiniLM-L-12-v2", cache_dir=cache_dir)
    
    def create_lightweight_embedder(self):
        """Create lightweight embedding system"""
        return LightweightEmbedder(self.load_spacy_model())
    
    def load_domain_vocabularies(self):
        """Load domain vocabularies"""
        vocab_path = self.models_dir / "vocabularies" / "domain_keywords.pkl"
        try:
            with open(vocab_path, "rb") as f:
                return pickle.load(f)
        except:
            return self._create_default_vocabularies()
    
    def _create_default_vocabularies(self):
        """Create comprehensive default vocabularies"""
        return {
            "Travel Planner": {
                "critical": ["itinerary", "schedule", "plan", "days", "group", "activities"],
                "high_priority": ["accommodation", "restaurant", "transport", "budget", "visit", "explore"],
                "job_specific": ["4 days", "college", "friends", "student", "group of 10", "trip"],
                "actionable": ["book", "reserve", "organize", "coordinate", "arrange", "prepare"]
            }
        }

class LightweightEmbedder:
    """Lightweight semantic embedding using only spaCy and basic math"""
    
    def __init__(self, nlp_model):
        self.nlp = nlp_model
        
    def encode(self, text):
        """Create embeddings using spaCy word vectors"""
        if not text or not text.strip():
            return np.zeros(96)
            
        doc = self.nlp(text[:500])
        
        vectors = []
        for token in doc:
            if (token.has_vector and not token.is_stop and 
                not token.is_punct and len(token.text) > 2):
                vectors.append(token.vector)
        
        if vectors:
            return np.mean(vectors, axis=0)
        else:
            return np.zeros(96)
    
    def similarity(self, text1, text2):
        """Calculate similarity between two texts"""
        vec1 = self.encode(text1)
        vec2 = self.encode(text2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return float(dot_product / (norm1 * norm2))

class SimpleTFIDF:
    """Simple TF-IDF implementation without scikit-learn"""
    
    def __init__(self, max_features=1000):
        self.max_features = max_features
        self.vocabulary = {}
        self.idf_values = {}
    
    def fit_transform(self, documents):
        """Fit TF-IDF on documents and return matrix"""
        # Build vocabulary
        all_words = []
        for doc in documents:
            words = self._tokenize(doc)
            all_words.extend(words)
        
        word_counts = Counter(all_words)
        # Keep most common words up to max_features
        self.vocabulary = {word: i for i, (word, _) in 
                          enumerate(word_counts.most_common(self.max_features))}
        
        # Calculate IDF values
        doc_count = len(documents)
        for word in self.vocabulary:
            containing_docs = sum(1 for doc in documents if word in self._tokenize(doc))
            self.idf_values[word] = np.log(doc_count / (containing_docs + 1))
        
        # Create TF-IDF matrix
        matrix = []
        for doc in documents:
            vector = self._document_to_vector(doc)
            matrix.append(vector)
        
        return np.array(matrix)
    
    def transform(self, documents):
        """Transform documents using fitted vocabulary"""
        matrix = []
        for doc in documents:
            vector = self._document_to_vector(doc)
            matrix.append(vector)
        return np.array(matrix)
    
    def _tokenize(self, text):
        """Simple tokenization"""
        text = text.lower()
        words = re.findall(r'\b[a-z]{2,}\b', text)
        return words
    
    def _document_to_vector(self, document):
        """Convert document to TF-IDF vector"""
        words = self._tokenize(document)
        word_count = len(words)
        
        vector = np.zeros(len(self.vocabulary))
        
        if word_count == 0:
            return vector
        
        word_freq = Counter(words)
        
        for word, freq in word_freq.items():
            if word in self.vocabulary:
                tf = freq / word_count
                idf = self.idf_values.get(word, 0)
                vector[self.vocabulary[word]] = tf * idf
        
        return vector

def cosine_similarity_simple(a, b):
    """Simple cosine similarity calculation"""
    dot_product = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    return dot_product / (norm_a * norm_b)
