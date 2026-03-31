import numpy as np

"""
    analyzer.py computes the cosine similarity between the scope embedding and all the abstracts embeddings.
    The output will tell us how much an article is coerent or not with the scope. This value will be the alignment score.
    There's also a function which shows basic stats about the output obtained.
"""



class Analyzer:
    def __init__(self, scope_embedding, article_embeddings):
        self.scope_embedding = scope_embedding
        self.article_embeddings = article_embeddings

    def cosine_similarity(self, vector1, vector2):
        num = np.dot(vector1, vector2)
        denom = np.linalg.norm(vector1) * np.linalg.norm(vector2)
        return num / denom if denom != 0 else 0.0

    def compute_scores(self):
        scores = [self.cosine_similarity(self.scope_embedding, emb) 
                  for emb in self.article_embeddings]
        return np.array(scores)

    def statistics(self, scores):
        return {
            "mean": float(np.mean(scores)),
            "std": float(np.std(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores))
        }
