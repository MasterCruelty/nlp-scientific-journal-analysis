import requests
import pandas as pd
import time
import re
import html

"""
    get-dataset.py works as an extractor of articles from a certain Journal of our choice.
    * First of all there is need to get the ISSN of the Journal and the range of years. 
    * Then we can do the correct API call to get the amount of articles of our interest.
    * In the end the amount of data will get a first refine and converted into a dataset.

"""



#fetching articles in json format by api call and return array.
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

        #no items -> we already finished -> break
        items = data["message"]["items"]
        if not items:
            break
        
        all_papers += articles_to_array(items,temp_array)
        
        offset += rows
        time.sleep(1)
    return all_papers 

#aux function to conver to array json articles extracted by api call
def articles_to_array(articles_json,articles_array):
    #for each item obtained, we get a few fields of interest.
    for item in articles_json:
        title = item.get("title", [""])[0]
        abstract_raw = item.get("abstract")
        #without any abstract the item is useless, otherwise we clean it from html tags
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

#aux function which clean the raw html abstract format
def clean_abstract(raw):
    #remove  XML/HTML
    text = re.sub("<.*?>", "", raw)
    #decode HTML entity (&amp;, &lt;, etc.)
    text = html.unescape(text)
    return text.strip()



#build dataset given the articles extracted by api call
def build_dataset(articles):
    df = pd.DataFrame(articles)
    df.to_csv("dataset.csv", index=False)
    print("Total articles:", len(df))


##############################
# execution 
##############################

#issn number of the journal (Frontiers in Artificial Intelligence)
issn = "26248212"   
url = f"https://api.crossref.org/journals/{issn}/works"

#range of years
start_date = "2021-01-01"
end_date = "2025-12-31"

#number of rows
rows = 1000

articles = fetch_articles(start_date,end_date,rows,url)
build_dataset(articles)