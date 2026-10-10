import os
import sys
import re
from sentence_transformers import SentenceTransformer, util

# Ensure backend root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

class TaskComplexityParser:
    """Hybrid NLP Parser combining semantic embeddings & technical jargon density."""

    def __init__(self):
        print("Loading SentenceTransformer model ('all-MiniLM-L6-v2')...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Anchor text clusters defining high vs low cognitive demand
        self.high_complexity_anchors = [
            "debug distributed systems memory leak deadlock race condition",
            "implement machine learning pipeline neural network optimization",
            "architect database schema integer linear programming solver",
            "refactor complex C++ backend algorithms data structures"
        ]
        self.low_complexity_anchors = [
            "reply to routine team emails and slack messages",
            "update documentation text grammar formatting README",
            "organize desktop files clean up folder structure",
            "attend brief daily status standup meeting sync"
        ]

        # Pre-compute anchor vector embeddings
        self.high_anchor_vecs = self.model.encode(self.high_complexity_anchors, convert_to_tensor=True)
        self.low_anchor_vecs = self.model.encode(self.low_complexity_anchors, convert_to_tensor=True)

        # Pattern for technical terminology
        self.jargon_pattern = re.compile(
            r'\b(api|async|database|sql|algorithm|pipeline|bug|refactor|schema|query|model|thread|deploy|test|docker|git|class|function|index)\b',
            re.IGNORECASE
        )

    def calculate_jargon_density(self, text: str) -> float:
        """Calculates ratio of technical keywords to total word count."""
        words = text.split()
        if not words:
            return 0.0
        matches = len(self.jargon_pattern.findall(text))
        return min(matches / len(words), 1.0)

    def parse_complexity(self, title: str, description: str = "") -> float:
        """Computes a composite cognitive complexity weight W_j between 0.0 and 1.0."""
        full_text = f"{title} {description}".strip()
        if not full_text:
            return 0.5  # Neutral default

        # 1. Semantic Embedding Similarity
        text_vec = self.model.encode(full_text, convert_to_tensor=True)
        
        high_sim = float(util.cos_sim(text_vec, self.high_anchor_vecs).max())
        low_sim = float(util.cos_sim(text_vec, self.low_anchor_vecs).max())

        # Normalize relative similarity to range [0, 1]
        raw_semantic_score = (high_sim - low_sim + 1.0) / 2.0
        semantic_score = max(0.0, min(raw_semantic_score, 1.0))

        # 2. Technical Jargon Density
        jargon_density = self.calculate_jargon_density(full_text)

        # 3. Hybrid Weighted Combination (70% Semantic Vector, 30% Jargon)
        final_weight = (0.7 * semantic_score) + (0.3 * jargon_density)
        return round(max(0.05, min(final_weight, 1.0)), 2)


if __name__ == "__main__":
    parser = TaskComplexityParser()

    sample_tasks = [
        ("Fix race condition in async database connection pool", "Investigate thread locks and deadlock traces in SQLAlchemy"),
        ("Reply to team Slack messages", "Check general channel for updates"),
        ("Build LightGBM time-series energy forecasting model", "Train on rolling fatigue features and evaluate RMSE"),
        ("Reorganize desktop download folder", "")
    ]

    print("\n--- NLP Task Complexity Parsing Test ---")
    for title, desc in sample_tasks:
        weight = parser.parse_complexity(title, desc)
        print(f"Task: '{title}'")
        print(f" -> Cognitive Complexity Weight (W_j): {weight} / 1.0\n")