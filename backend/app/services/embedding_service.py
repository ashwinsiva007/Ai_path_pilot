import re
import math
from collections import Counter

# Try importing Sentence Transformers
try:
    from sentence_transformers import SentenceTransformer, util
    _HAS_ST = True
except ImportError:
    _HAS_ST = False
    print("WARNING: sentence-transformers not installed. Using TF-IDF fallback for semantic matching.")

class EmbeddingService:
    def __init__(self):
        self.model = None
        if _HAS_ST:
            try:
                # Load a lightweight, fast model
                self.model = SentenceTransformer('all-MiniLM-L6-v2')
            except Exception as e:
                print(f"Error loading SentenceTransformer: {e}. Falling back to TF-IDF.")
                self.model = None

    def calculate_similarity(self, text1: str, text2: str) -> float:
        if not text1 or not text2:
            return 0.0

        # If Sentence Transformers model loaded successfully, use it
        if self.model:
            try:
                emb1 = self.model.encode(text1, convert_to_tensor=True)
                emb2 = self.model.encode(text2, convert_to_tensor=True)
                cos_sim = util.cos_sim(emb1, emb2).item()
                # Scale from [-1, 1] to [0, 100]
                similarity = max(0.0, cos_sim) * 100
                return round(similarity, 1)
            except Exception as e:
                print(f"SentenceTransformer embedding error: {e}. Falling back to TF-IDF.")

        # Fallback: TF-IDF Cosine Similarity in Pure Python
        return self._tfidf_similarity(text1, text2)

    def _tfidf_similarity(self, text1: str, text2: str) -> float:
        def get_tokens(text):
            return re.findall(r'\w+', text.lower())

        words1 = get_tokens(text1)
        words2 = get_tokens(text2)

        c1 = Counter(words1)
        c2 = Counter(words2)

        vocab = set(c1.keys()).union(set(c2.keys()))

        # Cosine similarity calculation
        dot_product = sum(c1[w] * c2[w] for w in vocab)
        mag1 = math.sqrt(sum(c1[w]**2 for w in c1))
        mag2 = math.sqrt(sum(c2[w]**2 for w in c2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        similarity = (dot_product / (mag1 * mag2)) * 100
        return round(similarity, 1)

embedding_service = EmbeddingService()
