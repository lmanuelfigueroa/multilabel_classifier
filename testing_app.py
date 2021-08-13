import streamlit as st
import operator
import sys
import numpy
import spacy
from spacy.tokens  import DocBin
import random
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
import time




tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

screen_tags = ['','aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']


def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 3
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    for i in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        st.write(f"tag:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")

def test_model(main) -> None:

    TESTING_SAMPLES = 3

    nlp = spacy.load("model_output_exclusive/model-last")


    for tag in tags:
        st.write("\n===========================================================================\n")

        tag_file = open("./model_data/"+ tag + "/test.txt","r",encoding = "utf-8")
    
        st.write("TESTING " + tag.upper() + " CATEGORY\n")

        text = []
        for line in tag_file:
            text.append(line)
        print("\n")

        for i in range(TESTING_SAMPLES):
            st.write(text[i].strip())
            doc = nlp(text[i])
            print_top_tags(doc.cats)
            print("\n")
        tag_file.close()

def top_tag(tags : dict) -> str:
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)
    pair = next(pair_iter)
    #print(f"tag:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")
    return pair[0]

def display_mode(mode,title_holder,main_holder) -> None:
    
    
    if mode == "View Current Corpus Stats":
        display_current_corpus(title_holder,main_holder)
        #display information of current corpus and ask to select tags
        
    elif mode == "Upload Corpus":
        title_holder.title("Upload corpus test")
        #ask to upload file, select tags and percentage 
        
    elif mode == "View Confusiong Matrix":
        title_holder.title("Multilabel Classifier Results Confusion Matrix")
        display_matrix()
    else:
        display_main_page(title_holder,main_holder)

def display_current_corpus(title_holder,main_holder) -> None:
    title_holder.title("Search Documents by Tags")
    main = st.form("current")
    selected_tag = main.selectbox("Select Tag to Search Documents",screen_tags)
    st.session_state.tag = selected_tag
    number = main.number_input("Enter a percentage: ex: 50",min_value = 0, max_value = 100, value = 50)
    st.session_state.percentage = number
    submit_button = main.form_submit_button("Submit")
    if submit_button:
        print(selected_tag + " and "+ number)
    else:
        main.write("exiting")

#resets the contents of the main page 
def display_main_page(title, main) -> None:
    title.title("USHMM Oral Testimony MultiLabel Classifier")
    main.write("View Items")
    

def display_app() -> None:

    #creating holders that will add and remove content on title and main page depending on the selected page
    title_holder = st.empty()
    main_holder = st.empty()

    display_main_page(title_holder,main_holder)

    #side bar widgets
    side_bar_form = st.sidebar.form("Options")
    mode_option = side_bar_form.selectbox("Pick Mode to Use:", ("Home","View Current Corpus Stats", "Upload Corpus","View Confusiong Matrix"))
    search = side_bar_form.form_submit_button("Search")

    #check to see if button was pressed and passes selected mode
    if search:
        #removing the contents of the main page
        main_holder.empty()
        display_mode(mode_option,title_holder,main_holder)
    else:
        side_bar_form.write("Nothing pressed")

    
   
    


if __name__ == "__main__":
    display_app()