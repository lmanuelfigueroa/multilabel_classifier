import spacy
import operator
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff
import streamlit as st


tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']


def app() -> None:
    st.title("Confusion Matrix")
    matrix = display_matrix()
    st.plotly_chart(matrix,use_container_width=True)

@st.cache(allow_output_mutation = True)
def display_matrix():

    PREDICTION_SAMPLES = 100
    true_values = []
    prediction_values = []
    nlp = spacy.load("model_output_exclusive/model-last")

    
    for tag in tags:

        file = open("model_data/"+ tag +"/test.txt","r",encoding = "utf-8")

        for i in range(PREDICTION_SAMPLES):
            true_values.append(tag)
            text = file.readline()
            top_tags = nlp(text)
            first_tag = top_tag(top_tags.cats)
            prediction_values.append(first_tag)
        
        file.close()

    matrix = confusion_matrix(true_values,prediction_values,labels = tags)
    figure = create_heat_map(matrix)
    return figure
    



def create_heat_map(matrix):

    
    anotated_matrix= matrix.tolist()
    matrix_text = [[str(y) for y in x] for x in anotated_matrix] 

    #set up figure 
    fig = ff.create_annotated_heatmap(anotated_matrix, x=tags, y=tags, 
    annotation_text=matrix_text, colorscale='Viridis')


    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="white",size=14),
                        x=0.5,
                        y=-0.08,
                        showarrow=False,
                        text="Predicted value",
                        xref="paper",
                        yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="white",size=14),
                        x=-.10,
                        y=.50,
                        showarrow=False,
                        text="Expected value",
                        textangle=-90,
                        xref="paper",
                        yref="paper"))

    # adjust margins to make room for yaxis title
    fig.update_layout(margin=dict(t=100, l=150))

    # add colorbar
    fig['data'][0]['showscale'] = True
    return fig
    #fig.show()

    print("DONE CREATING CONFUSION MATRIX")

def top_tag(tags : dict) -> str:
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)
    pair = next(pair_iter)
    #print(f"tag:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")
    return pair[0]

