from os import link
import streamlit as st
import glob
import requests 
from bs4 import BeautifulSoup



tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']


def display_app():
    path = "new_ocr/*txt"

    files = glob.glob(str(path))

    transcripts = []
    dic = {"one":1 , "two":0, "three":4}
    

    count = 0
    for file in files:
        
        temp = file.split("\\")[1].replace(".txt","")
        rg_num = temp.split("_")[0]
        temp = temp +".pdf#page6"
        url = f"https://collections.ushmm.org/oh_findingaids/{temp}"
        transcript = f'<a target="_blank" onclick="find({rg_num});" href="{url}">{rg_num}</a>' 
        transcripts.append(url)
        # with open(file, "r",encoding= "utf-8") as f:
        #     data = f.read()
        
    links = [] 
    for items in transcripts:
        reqs = requests.get(items)
        soup = BeautifulSoup(reqs.text, "html.parser")
        element = str(soup.find_all('title'))
        if "Not Found" in element:
           
            links.append(items)

        # for title in soup.find_all("title"):
        #     print(title.get_text())

    
    # for item in transcripts:
    #     st.write(item,unsafe_allow_html = True)

if __name__ == "__main__":
    display_app()