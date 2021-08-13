import streamlit as st
from spacy.lang.en import English
import operator
import spacy
import glob

tags = ['aid', 'american', 'army', 'buildings', 'camp', 'family', 'fear', 'food', 
'ghetto', 'government', 'hiding', 'hospital', 'hunger', 'Jewish', 'kill','Nazi', 'police', 'polish', 'prisoners', 'religion', 
'relocation', 'russian', 'school', 'shooting', 'sick', 'survive', 'synagogue', 'war', 'work']



screen_tags = ['','aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def app() -> None:
    st.title("Search Corpus")
    main = st.form("current")
    selected_tag = main.selectbox("Select Tag to Search Documents",screen_tags)
    #st.session_state.tag = selected_tag
    percentage = main.number_input("Enter a percentage: ex: 50",min_value = 0, max_value = 100, value = 50)
    #st.session_state.percentage = number
    submit_button = main.form_submit_button("Submit")
    if submit_button:
        st.write(selected_tag + " and "+ str(percentage))
        load_model(selected_tag,percentage)



def load_model(tag, percentage) -> None:
    
    nlp = English()

    path = "single_test_reading/*.txt"
    #path = "data/single_test_reading/*.txt"
    files = glob.glob(str(path))
    display_info = None
    
    for file in files:
            with open(file, "r",encoding= "utf-8") as f:
                data = f.read()
                process_document(nlp,data,tag, percentage)

def process_document(nlp,data,tag,percentage) -> None:

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
    with open ("testing_sentences.txt", "w", encoding="utf-8") as f:
        for sent in doc.sents:
            text = remove_accents(str(sent.text))
            doc = nlp_labels(text)

            
            first_tag = top_tag(doc.cats)
            if doc.cats[first_tag] > PERCENTAGE_CONSIDER_TAG:
                num_of_tags_found +=1
                label_dict[first_tag] = label_dict[first_tag] + 1
            f.write(text+"\n")

    st.write(f"The documents contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned on {round(PERCENTAGE_CONSIDER_TAG*100)}% tag requirement\n")

    st.write(label_dict)
    print_top_tags(label_dict)

def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 3
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    top_tags = []
    
    for i in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        top_tags.append(pair[0])
    
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
