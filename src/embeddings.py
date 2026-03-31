from sentence_transformers import SentenceTransformer

"""
    embeddings.py takes a list of strings (abstracts or scope) and returns
    the corresponding embeddings using a SentenceTrasformer model.

    Model: allenai-specter
    This model is trained on scientific papers.

    1. Create an instance of EmbeddingsGenerator.
    2. We pass the list of abstracts to obtain the embeddings.
    3. We pass the scope to obatin its embedding too.
"""


class EmbeddingGenerator:
    def __init__(self, model_name="allenai-specter"):
        self.model = SentenceTransformer(model_name)

    def encode_texts(self, texts):
        """
        texts: list of abstracts (preprocessed) or single-element list containing scope.
        batch_size: controls memory usage during encoding.
        show_progress: set True to display tqdm progress bar.
        return: array numpy with embeddings.
        """
        return self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True,
            convert_to_numpy=True
        )