import requests
import pandas as pd
import time
import re
import html

#issn number of the journal
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

