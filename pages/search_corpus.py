import streamlit as st
from csv import reader
import pandas as pd
import ast

#the list of tags contains an empty string in the first element to 
# prevent the selector from automatically selecting and running the first element in the list
screen_tags = ['','aid', 'american','army', 'buildings', 'camp', 'family', 'fear', 'food', 
'ghetto','government', 'hiding','hospital', 'hunger',  'Jewish', 'kill','Nazi', 'police','polish', 'prisoners',  
 'religion','relocation','russian', 'school','shooting','sick','survive', 'synagogue','war','work']

def app() -> None:
    st.title("Search Corpus")
    main = st.form("current")
    selected_tag = main.selectbox("Select Tag to Search Documents",screen_tags)
    top_number = main.number_input("How many of the top tags do you want to see? "
    "Example: 3, Results will display documents where choosen tag is in the top 3 tags",min_value = 1, max_value = 29, value = 3)
    submit_button = main.form_submit_button("Submit")
    if submit_button:
        read_model_results(selected_tag,top_number)



def read_model_results(tag, top_number) -> None:
    

    #the results of the model processing the files from the app are saved in the csv file all_tags.csv, this will improve the speed of the app
    csv_path = "csv_files/all_tags.csv"

    documents = []
    with open(csv_path,"r") as line:
        row = reader(line)

        #removing the first line which is the column names 
        next(row)

        #iterating the csv files and coverting the string values to strings for document RG and tuples for tag percentages
        for col in row:
            documents.append((col[1],ast.literal_eval(col[2])))

    #narrowing down the list tags for the results according to how many tags the user wants to see
    reduced_tag_percentages = reduce_tag_results(documents,top_number)

    results = []
    rg_links = []

    #iterating through the list and searching for the documents where the tap is in the top n tag percentages
    for doc in reduced_tag_percentages:

        #creating the links to the documents using the rg numbers
        doc_link = doc[0] + "_trs_en.pdf#page6"
        url = f"https://collections.ushmm.org/oh_findingaids/{doc_link}"
        link = f'<a target="_blank" onclick="find({doc[0]});" href="{url}">{doc[0]}</a>' 
        
        #saving the rg numbers in one list and the list of tags in another list for the dataframe
        for i in range(top_number):
            if doc[1][i][0] == tag:
                rg_links.append(link)
                results.append(doc[1])

    #checking to see if the list contains results
    results = clean_results(results)
    if len(results) == 0:
        st.write("No documents were found with the given parameters. Expand the number of tags to display")
    else:
        st.write(f"{len(results)} documents found with the tag \"{tag.capitalize()}\" in the top {top_number} percentages")
        table_data = pd.DataFrame({'Testimony':rg_links,'Top Tags':results})
        table_data = table_data.to_html(escape = False)
        st.write(table_data,unsafe_allow_html = True)


#this function will print the results more visuali pleasing for the user by capitalizing the name of the tag and adding percent sign to float value
def clean_results(results):

    clean_results = []
    
    for dictionary in results:
        temp = []
        for tag in dictionary:
            temp.append((tag[0].capitalize(),str(tag[1]) + "%"))

        clean_results.append(temp)
    return clean_results


#reduces the number of tags to display in the results
def reduce_tag_results(documents, top_number):

    small_doc_list = []
        
    #iterating through the tag percentages of each list 
    for item in documents:
        dict_pairs = item[1].items()
        pair_iter =  iter(dict_pairs)
        temp = []
        
        #geting the top n tags asked by the user
        for i in range(top_number):
            pair = next(pair_iter)
            temp.append(pair)
        small_doc_list.append((item[0],temp))
    
    return  small_doc_list