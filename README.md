[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/lmanuelfigueroa/ushmm_text_classification_app/main/app.py)

# Overview

This project was part of my undergrad internship with the Smithsonian Data Science Lab and United States Holocaust Memorial Museum. The goal of the project is to create a text classifier to categorize Holocaust documents to facilitate the searching for researchers  when looking for specific documents.

# Contributors
* Luis M. Figueroa 
* William Mattingly (Mentor)

## Languages
* Python 


## Program and Code requisites 
* Python 3.8 or above(Errors install gensim and Scipy can come up when using Python 3.7 with DDL files and OS ERRORS) [See link for discussing](https://github.com/scipy/scipy/issues/11826) 
* SpaCy Library for sentesizer and loading model
* skleanr to plot the confusion matrix 
* pandas to create data frames for confusion matrix


## Getting Started
* Install Python 3.8 or above
* Install libraries from above using "pip install name of libray

## Explain Files and Folders
* Folder csv_files contains the results from the text classifier model on the documents in new_ocr folder
* new_ocr folder contains the documents that the model searches given what the user is looking for.
* model_outout_exclusive contains the data from the mutually exclusive text classifier model used to process the documents the user uploaded. 

## Structure of App 
* Source to create framework to create the multi page streamlit app [Source of Framework](https://github.com/upraneelnihar/streamlit-multiapps)

## Run App 
* Use command on terminal to run the app ``` streamlit run app.py```