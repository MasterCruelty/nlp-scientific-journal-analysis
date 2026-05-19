import requests
import pandas as pd
import time
import re
import html

"""
    get-dataset.py works as an extractor of articles from a certain Journal of our choice.
    * First of all there is need to obtain the ISSN of the Journal and it's needed to select a range of years.
    * Then we use Crossref API to get the articles of our interest.
    * At the end the amount of data will get a first refine and converted into a dataset.
"""


def fetch_articles(start_date, end_date, rows, url):
    """Fetch articles via Crossref API, paginating until no items remain. Returns a list of extracted articles."""
    offset = 0
    all_papers = []
    while True:
        params = {
            "filter": f"from-pub-date:{start_date},until-pub-date:{end_date}",
            "rows": rows,
            "offset": offset,
        }
        
        resp = requests.get(url, params=params)
        items = resp.json()["message"]["items"]
        
        if not items:
            break
        
        all_papers.extend(parse_articles(items))
        
        offset += rows
        time.sleep(1)
    return all_papers


def parse_articles(articles_json):
    """Extract relevant fields from raw API items; skip entries without an abstract. Returns refined list of articles."""
    articles = []
    for item in articles_json:
        abstract_raw = item.get("abstract")
        if not abstract_raw:
            continue
        
        articles.append({
            "title": item.get("title", [""])[0],
            "abstract": clean_abstract(abstract_raw),
            "year": item.get("issued", {}).get("date-parts", [[None]])[0][0],
            "doi": item.get("DOI"),
        })
    return articles


def clean_abstract(raw):
    """Strip XML/HTML tags and decode HTML entities from an abstract string."""
    text = re.sub("<.*?>", "", raw)
    return html.unescape(text).strip()


def build_dataset(articles):
    data = pd.DataFrame(articles)
    data.to_csv("dataset_test.csv", index=False)
    print("Total articles:", len(data))


##############################
# execution 
##############################

if __name__ == "__main__":
    #issn number of the journal (Frontiers in Artificial Intelligence)
    issn = "26248212"   
    url = f"https://api.crossref.org/journals/{issn}/works"

    #range of years
    start_date = "2021-01-01"
    end_date = "2025-12-31"

    #number of rows
    rows = 1000

    #Collecting abstract of articles from target journal
    print("Collecting articles...")
    articles = fetch_articles(start_date,end_date,rows,url)
    print("Extraction completed.")
    build_dataset(articles)    