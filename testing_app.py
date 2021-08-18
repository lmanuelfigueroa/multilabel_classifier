from os import link
from numpy import TooHardError
import streamlit as st
import glob
from csv import reader
import ast
import operator


tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']


def display_app():

    references = []
    path = "new_ocr/*txt"
    TOP_NUMBER = 3
    csv_path = "csv_files/all_tags.csv"
    tag = "buildings"

    with open(csv_path,"r") as line:
        row = reader(line)

        next(row)
        for col in row:
            references.append((col[1],ast.literal_eval(col[2])))
    
    #for line in references:
        #print(line[1])
        
    #print(references)
    smaller = reduce_dict(references,TOP_NUMBER,tag)
    
    results = []
    count = 0
    print(len(smaller))
    for reference in smaller:
        #print(reference)
        for i in range(TOP_NUMBER):
            if reference[1][i][0] == tag:
                results.append(reference)
                
    print(len(results))
    print(results)


def reduce_dict(reference,limit,tag):
        
    
    small_reference = []
        #sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    for item in reference:
        dict_pairs = item[1].items()
        pair_iter =  iter(dict_pairs)
        small_dict = []
        #print(item)
        for i in range(limit):
            pair = next(pair_iter)
            small_dict.append(pair)
            # if tag == pair[0]:
            #     small_dict.append(pair)
        small_reference.append((item[0],small_dict))
    
    return small_reference
    # count = 0
    # for file in files:
        
    #     temp = file.split("\\")[1].replace(".txt","")
    #     rg_num = temp.split("_")[0]
    #     temp = temp +".pdf#page6"
    #     url = f"https://collections.ushmm.org/oh_findingaids/{temp}"
    #     transcript = f'<a target="_blank" onclick="find({rg_num});" href="{url}">{rg_num}</a>' 
    #     transcripts.append(url)
    #     # with open(file, "r",encoding= "utf-8") as f:
    #     #     data = f.read()
        
    # links = [] 
    # for items in transcripts:
    #     reqs = requests.get(items)
    #     soup = BeautifulSoup(reqs.text, "html.parser")
    #     element = str(soup.find_all('title'))
    #     if "Not Found" in element:
           
    #         links.append(items)

        # for title in soup.find_all("title"):
        #     print(title.get_text())

    
    # for item in transcripts:
    #     st.write(item,unsafe_allow_html = True)

if __name__ == "__main__":
    display_app()