  
import streamlit as st
from multiapp import MultiApp
from pages import confusion_matrix,search_corpus,upload_corpus,home

app = MultiApp()
st.title("USHMM Oral Testimony MultiLabel Classifier")
"""
### Features on App

- Search Corpus
    - Displays the documents that have high percentages of the topic of interest.
- Upload Corpus
    - Upload your own files and page will display the percentages of topics found in each document.
- Confusion Matrix
    - Displays the accuracy of the model used on 50 text samples in a Confusion Matrix.
"""


# Add all your application here
app.add_app(" ",home.app)
app.add_app("Search Corpus", search_corpus.app)
app.add_app("Upload Corpus", upload_corpus.app)
app.add_app("Display Matrix",confusion_matrix.app)


# The main app
app.run()