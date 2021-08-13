  
import streamlit as st
from multiapp import MultiApp
from pages import confusion_matrix,search_corpus,upload_corpus,home

app = MultiApp()
st.title("USHMM Oral Testimony MultiLabel Classifier")
st.write("View Items")


# Add all your application here
app.add_app(" ",home.app)
app.add_app("Search Corpus", search_corpus.app)
app.add_app("Upload Corpus", upload_corpus.app)
app.add_app("Display Matrix",confusion_matrix.app)


# The main app
app.run()