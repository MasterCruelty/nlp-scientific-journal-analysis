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



"""
    This function extracts articles by api call in json format and return an array of articles
"""
def fetch_articles(start_date,end_date,rows,url):
    offset = 0
    all_papers = []
    #fetching articles increasing offset page by page until we don't get any articles
    while True:
        temp_array = []
        params = {
            "filter": f"from-pub-date:{start_date},until-pub-date:{end_date}",
            "rows": rows,
            "offset": offset
        }

        resp = requests.get(url, params=params)
        data = resp.json()

        items = data["message"]["items"]
        #no items -> we already finished -> break
        if not items:
            break
        
        all_papers += articles_to_array(items,temp_array)
        
        offset += rows
        time.sleep(1)
    return all_papers 


"""
    This function takes raw articles data extracted by api call.
    It takes a few fields of interest and convert to array.
"""
def articles_to_array(articles_json,articles_array):
    for item in articles_json:
        title = item.get("title", [""])[0]
        abstract_raw = item.get("abstract")
        #without any abstract the item is useless and we ignore it, otherwise we clean it from html tags
        if not abstract_raw:
            continue
        abstract_cleaned = clean_abstract(abstract_raw)
            
        year = item.get("issued", {}).get("date-parts", [[None]])[0][0]
        doi = item.get("DOI")

        articles_array.append({
            "title": title,
            "abstract": abstract_cleaned,
            "year": year,
            "doi": doi
        })
    return articles_array

"""
    This function removes any html tags from the raw abstract and return a clean string version.
"""
def clean_abstract(raw):
    #remove  XML/HTML
    text = re.sub("<.*?>", "", raw)
    #decode HTML entity (&amp;, &lt;, etc.)
    text = html.unescape(text)
    return text.strip()

"""
    This function convert the array of articles in a csv dataset
"""
def build_dataset(articles):
    df = pd.DataFrame(articles)
    df.to_csv("dataset.csv", index=False)
    print("Total articles:", len(df))


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
    articles = fetch_articles(start_date,end_date,rows,url)
    build_dataset(articles)