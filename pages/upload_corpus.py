import streamlit as st
from spacy.lang.en import English
import operator
import spacy
from io import StringIO


tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def app() -> None:
    st.title("Upload Corpus")

    upload_files = st.file_uploader("Enter a file:",accept_multiple_files=True)

    if upload_files is not None:
        for file in upload_files:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            string_data = stringio.read()
            process_document(string_data,file.name)
            #st.write(string_data)
        
def process_document(document,file_name) -> None:

    nlp = English()
    PERCENTAGE_CONSIDER_TAG = 0
    label_dict = dict.fromkeys(tags,0)
    nlp_labels = spacy.load("model_output_exclusive/model-last")
    
    if nlp.pipe_names != []:
        nlp.remove_pipe("sentencizer")

    nlp.max_length = 174214790
    nlp.add_pipe('sentencizer')
    doc = nlp(document, disable=['parser', 'tagger', 'ner'])

    num_of_sentences = len(list(doc.sents))

    num_of_tags_found = 0
    for sent in doc.sents:
        text = remove_accents(str(sent.text))
        doc = nlp_labels(text)
    
        first_tag = top_tag(doc.cats)
        if doc.cats[first_tag] > PERCENTAGE_CONSIDER_TAG:
            num_of_tags_found +=1
            label_dict[first_tag] = label_dict[first_tag] + 1
                
    #st.write(f"Document {file_name} contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned on {round(PERCENTAGE_CONSIDER_TAG*100,1)}% tag requirement\n")
    st.write(f"Document {file_name} contains {num_of_sentences} sentences and {num_of_tags_found} tags were assigned")
    
    #getting the percentage of tags for the document
    for tag in label_dict:
        label_dict[tag] = round(label_dict[tag]*100/num_of_tags_found,1)

    print_top_tags(label_dict)


def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 5
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    top_tags = []
    
    for i in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        top_tags.append(pair)

    st.write(f"The top { NUMB_OF_TAGS} tags in the document are {top_tags}\n")


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
