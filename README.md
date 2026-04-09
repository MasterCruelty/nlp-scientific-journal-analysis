# Analyzing Thematic Alignment in Scientific Journals

## Usage

### 1. Dataset population
Run get-dataset.py located in the `dataset` folder to retrieve articles from the selected scientific journal.
```bash
python dataset/get-dataset.py
```

### 2. Run the pipeline
Execute main.py located in the `src` folder. This will run the full pipeline and generate an updated dataset containing the alignment score for every article.
```bash
python src/main.py
```

### 3. Analyze results
Once the execution has finished, it is possible to view the results graphically.

1. Open the Results.ipynb notebook.

2. Run all cells to generate and view the visual reports.


## Reusability for other Journals

The code is designed to be adaptable to any scientific journal available via Crossref API.

1. ISSN Code: Obtain the ISSN code of the desired journal and insert it into the dataset/get-dataset.py script.

2. Journal Scope: Retrieve the official Scope text of the journal and save it as a .txt file inside the dataset folder.

    1. Sotto-elemento (usa 4 spazi o un tab)
    2. Sotto-elemento
