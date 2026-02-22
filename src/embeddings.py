from sentence_transformers import SentenceTransformer

"""
    embeddings.py taks a list of string(our set of articles's abstract) and return
    the corresponding embeddings using the SentenceTrasformer model.
    There's need to create an instance of EmbeddingsGenrator, then we pass the list of 
    abstracts already preprocessed to obtain the embeddings.
    Then we pass in a second moment the scope alrady preprocessed to obtain its embedding too.
"""


class EmbeddingGenerator:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def encode_texts(self, texts):
        """
        texts: list of abstracts already preprocessed or single element list containing scope
        return: array numpy with embeddings.
        """
        return self.model.encode(texts, convert_to_numpy=True)
