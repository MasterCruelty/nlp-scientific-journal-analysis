import requests
import pandas as pd
import time
import re
import html

#issn number of the journal (Frontiers in Artificial Intelligence)
issn = "26248212"   

#range of years
start_date = "2021-01-01"
end_date = "2025-12-31"

#api url for the get call
url = f"https://api.crossref.org/journals/{issn}/works"

#number of rows; initializing offset for pages; initializing array of all papers we will get.
rows = 1000
offset = 0
all_papers = []

#function which clean the raw html abstract format
def clean_abstract(raw):
    #remove  XML/HTML
    text = re.sub("<.*?>", "", raw)
    #decode HTML entity (&amp;, &lt;, etc.)
    text = html.unescape(text)
    return text.strip()

#fetching articles increasing offset page by page until we don't get any articles
while True:
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

    #for each item obtained, we get a few fields of interest.
    for item in items:
        title = item.get("title", [""])[0]
        abstract_raw = item.get("abstract")
        #without any abstract the item is useless, otherwise we clean it from html tags
        if not abstract_raw:
            continue
        abstract_cleaned = clean_abstract(abstract_raw)
        
        year = item.get("issued", {}).get("date-parts", [[None]])[0][0]
        doi = item.get("DOI")

        all_papers.append({
            "title": title,
            "abstract": abstract_cleaned,
            "year": year,
            "doi": doi
        })

    offset += rows
    time.sleep(1) 

df = pd.DataFrame(all_papers)
df.to_csv("frontiers_ai_2021_2025.csv", index=False)

print("Total articles:", len(df))
