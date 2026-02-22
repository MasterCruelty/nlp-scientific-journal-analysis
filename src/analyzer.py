import numpy as np

"""
    analyzer.py does the cosine similarity between the scope embedding and all the abstracts embeddings.
    The output will say us which article is coerent or not with the scope. This will be the score.
    There's also a function with base stats about the output obtained.
"""



class Analyzer:
    def __init__(self, scope_embedding, article_embeddings):
        self.scope_embedding = scope_embedding
        self.article_embeddings = article_embeddings

    def cosine_similarity(self, vec1, vec2):
        num = np.dot(vec1, vec2)
        denom = np.linalg.norm(vec1) * np.linalg.norm(vec2)
        return num / denom if denom != 0 else 0.0

    def compute_scores(self):
        scores = [self.cosine_similarity(self.scope_embedding, emb) 
                  for emb in self.article_embeddings]
        return np.array(scores)

    def statistics(self, scores):
        return {
            "mean": float(np.mean(scores)),
            "variance": float(np.var(scores)),
            "min": float(np.min(scores)),
            "max": float(np.max(scores))
        }
