#import streamlit as st
from spacy.lang.en import English
import operator
import spacy
import glob
import pandas as pd


# tags = ['aid','american', 'army', 'buildings', 'camp', 'family', 'fear', 'food', 
# 'ghetto', 'government', 'hiding', 'hospital', 'hunger', 'Jewish', 'kill','Nazi', 'police', 'polish', 'prisoners', 'religion', 
# 'relocation', 'russian', 'school', 'shooting', 'sick', 'survive', 'synagogue', 'war', 'work']

tags = ['family', 'fear', 'food', 'ghetto', 'government', 'hiding', 'hospital', 'hunger', 'Jewish', 'kill','Nazi', 'police', 'polish', 'prisoners', 'religion', 
'relocation', 'russian', 'school', 'shooting', 'sick', 'survive', 'synagogue', 'war', 'work','aid','american','army', 'buildings', 'camp' ]

screen_tags = ['','aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def app() -> None:
    #st.title("Search Corpus")
    #main = st.form("current")
    #selected_tag = main.selectbox("Select Tag to Search Documents",screen_tags)
    #percentage = main.number_input("Enter a percentage: ex: 50",min_value = 0, max_value = 100, value = 50)
    #submit_button = main.form_submit_button("Submit")
    #if submit_button:
    # for tag in tags:
    #     load_model(tag,0)
    load_model(0)



def load_model(percentage) -> None:
    
    nlp = English()

    #path = "single_test_reading/*.txt"
    #path = "testing_multilabel_corpus_reading/*.txt"
    path = "new_ocr/*.txt"
    files = glob.glob(str(path))
    rn_numbers = []
    result_tags = []

    for file in files:

        reference = file.split("\\")[1].replace(".txt","")
        rg_num = reference.split("_")[0]
        # reference = reference +".pdf#page6"
        # url = f"https://collections.ushmm.org/oh_findingaids/{reference}"
        # transcript = f'<a target="_blank" onclick="find({rg_num});" href="{url}">{rg_num}</a>' 

        
        with open(file, "r",encoding= "utf-8") as f:
            data = f.read()
            top_3_labels = process_document(nlp,data,percentage)
            #st.write(top_3_labels)
            #print(top_3_labels)
            #if top_3_labels[0][0] == tag or top_3_labels[1][0] == tag or top_3_labels[2][0] == tag:
            rn_numbers.append(rg_num)
            result_tags.append(top_3_labels)

    
    dict = {'rn_numbers':rn_numbers,'top_labels':result_tags}

    df = pd.DataFrame(dict)


    df.to_csv("csv_files/all_tags.csv")

    print(f"DONE CREATING CSV FILE")
    #df.to_csv("csv_files/"+tag.lower()+".csv")
    #print(f"DONE CREATING CSV FILE FOR {tag.upper()}")
    #table_data = pd.DataFrame({'Testimony':rn_numbers,'Top Tags':result_tags})
    #table_data = table_data.to_html(escape = False)
    #st.write(table_data,unsafe_allow_html = True)



def process_document(nlp,data,percentage) -> list:

    PERCENTAGE_CONSIDER_TAG = percentage/100
    label_dict = dict.fromkeys(tags,0)
    nlp_labels = spacy.load("model_output_exclusive/model-last")
    
    if nlp.pipe_names != []:
        nlp.remove_pipe("sentencizer")

    nlp.max_length = 174214790
    nlp.add_pipe('sentencizer')
    doc = nlp(data, disable=['parser', 'tagger', 'ner'])

    num_of_sentences = len(list(doc.sents))

    num_of_tags_found = 0
    for sent in doc.sents:
        text = remove_accents(str(sent.text))
        doc = nlp_labels(text)
    
        first_tag = top_tag(doc.cats)
        if doc.cats[first_tag] > PERCENTAGE_CONSIDER_TAG:
            num_of_tags_found +=1
            label_dict[first_tag] = label_dict[first_tag] + 1
                
    #st.write(f"The documents contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned on {round(PERCENTAGE_CONSIDER_TAG*100)}% tag requirement\n")
    #print(f"The documents contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned on {round(PERCENTAGE_CONSIDER_TAG*100)}% tag requirement\n")
    #getting the percentage of tags for the document
    for tag in label_dict:
        label_dict[tag] = round(label_dict[tag]*100/num_of_tags_found,1)


    sorted_d = dict( sorted(label_dict.items(), key=operator.itemgetter(1),reverse=True))
    #print(sorted_d)
    top_tags = sorted_d
    # dict_pairs = sorted_d.items()
    # pair_iter =  iter(dict_pairs)

    # top_tags = []

    # NUM_TOP_TAGS = 3
    
    # for i in range(NUM_TOP_TAGS):
    #     pair = next(pair_iter)
    #     top_tags.append(pair)
    
    return top_tags

def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 3
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    top_tags = []
    
    for i in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        top_tags.append(pair)
    
    st.write("\n")
    st.write(f"The top 3 most common tags in the document are {top_tags}")


def top_tag(tags : dict) -> str:
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)
    pair = next(pair_iter)
    return pair[0]

def remove_accents(text):
    #Polish letters
    letters= {
    'ł':'l', 'ą':'a', 'ń':'n', 'ć':'c', 'ó':'o', 'ę':'e', 'ś':'s', 'ź':'z', 'ż':'z',
    'Ł':'L', 'Ą':'A', 'Ń':'N', 'Ć':'C', 'Ó':'O', 'Ę':'E', 'Ś':'S', 'Ź':'Z', 'Ż':'Z',

    #Accent Vowels
    "à":"a", "á":"a", "â":"a", "ã":"a", "ä":"a", "å":"a", "æ": "ae",
    "À":"A", "Á":"A", "Â":"A", "Ã":"A", "Ä":"A", "Å":"A", "Æ": "ae",

    "è":"e", "é":"e", "ê":"e", "ë":"e",
    "È":"E", "É":"E", "Ê":"E", "Ë":"E",

    "ì":"i", "í":"i", "î":"i", "ï":"i",
    "Ì":"I", "Í":"I", "Î":"I", "Ï":"I",

    "ò": "o", "ó": "o", "ô": "o",  "õ": "o",  "ö": "o", "ø": "o",
    "Ò": "O", "Ó": "O", "Ô": "O",  "Õ": "O",  "Ö": "O", "Ø": "O",

    "ù": "u", "ú": "u",  "û": "u",  "ü": "u",
    "Ù": "U", "Ú": "U",  "Û": "U",  "Ü": "U",

    "ý": "y", "ÿ": "y",
    "Ý": "Y", "Ÿ": "Y",

    #Accent Cononants
    "ç": "c", "Ç": "C",
    "ß": "ss"
    }
    trans=str.maketrans(letters)
    result=text.translate(trans)
    return (result)

if __name__ == '__main__':
    app()