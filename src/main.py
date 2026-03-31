import pandas as pd
from preprocessing import preprocess_text
from embeddings import EmbeddingGenerator
from analyzer import Analyzer

"""
    main.py executes the full pipeline:

    1. Load the dataset.
    2. Preprocess abstracts of each article and the scope.
    3. Generation of embeddings
    4. Compute the cosine similarity between each abstract and the scope 
    5. Attach score for each article
    6. Show global and per-year statistics.
    7. Save new enriched dataset.
"""

def main():

    #######################################################
    # Load dataset
    #######################################################
    try:
        data = pd.read_csv("../dataset/dataset.csv")
    except FileNotFoundError:
        print("Dataset not found. Exiting...")
        return
    print(f"Loaded {len(data)} articles \nselected years:({sorted(data['year'].unique())})")

    #######################################################
    # preprocessing
    #######################################################
    data["abstract_processed"] = data["abstract"].apply(preprocess_text)
    
    try:
        with open("../dataset/aim_scope.txt", "r") as f:
            scope = f.read()
    except FileNotFoundError:
        print("Aim & Scope not found. Exiting...")
        return
    scope_processed = preprocess_text(scope)
    

    #######################################################
    # Generating embeddings
    #######################################################
    generator = EmbeddingGenerator()
    print("Encoding abstracts...")
    abstract_embeddings = generator.encode_texts(data["abstract_processed"].tolist())

    scope_embedding = generator.encode_texts([scope_processed])[0]

    #######################################################
    # Computing cosine similarity
    #######################################################
    analyzer = Analyzer(scope_embedding, abstract_embeddings)
    scores = analyzer.compute_scores()   
    data["alignment_score"] = scores

    #######################################################
    # Showing first basic results
    #######################################################
    stats = analyzer.statistics(scores)
    print("\nGlobal statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v:.4f}")
    
    print("\nAnalysis year by year:")
    year_stats = data.groupby("year")["alignment_score"].agg(["mean", "std", "count"])
    print(year_stats.to_string())

    #######################################################
    # Saving updated dataset which include computed scores.
    #######################################################
    data.to_csv("../dataset/dataset_with_scores.csv", index=False)
    print("\nSaved: dataset_with_scores.csv")


if __name__ == "__main__":
    main()