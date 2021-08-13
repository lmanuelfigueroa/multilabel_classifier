import sys
import numpy
import spacy
from spacy.tokens  import DocBin
import random
import operator
from sklearn.metrics import confusion_matrix
import plotly.figure_factory as ff


tags = ['aid', 'american','army', 'hunger','war' ,'buildings', 'work', 'camp', 'family', 'fear', 'food', 
'ghetto','relocation' ,'government', 'hiding','sick','hospital', 'shooting', 'kill','Nazi', 'police', 'prisoners','school', 'religion', 'Jewish', 
 'polish','russian', 'survive', 'synagogue']

def train_model() -> None:
    print("Training Model ....")

    nlp = spacy.load("en_core_web_sm")
    
    training_data = []
    validate_data = []

   
    # creating the training samples for model with tags
    for tag in tags:
        
        file = open("model_data/"+ tag +"/train.txt","r",encoding = "utf-8")

        for line in file:
            training_data.append((line,tag))
        file.close()

    training_data = random.sample(training_data,len(training_data))

    #creating the valid samples for model with tags

    for tag in tags:
        file = open("model_data/" + tag + "/valid.txt","r",encoding = "utf-8")

        for line in file:
            validate_data.append((line,tag))
        file.close()


    validate_data = random.sample(validate_data,len(validate_data))

    num_texts = 500

    #create the model 
    train_docs = make_docs(nlp,training_data)
    doc_bin = DocBin(docs=train_docs)
    doc_bin.to_disk("./model_data/train.spacy")

    valid_docs = make_docs(nlp,validate_data)

    doc_bin = DocBin(docs=valid_docs)
    doc_bin.to_disk("./model_data/valid.spacy")
    

    print("Done")




def make_docs(nlp, data):



    docs = []
    for doc, tag in nlp.pipe(data, as_tuples=True):

        #doc.cats["human_rights"] = 0
        doc.cats["war"] = 0
        doc.cats["work"] = 0
        doc.cats["school"] = 0
        doc.cats["russian"] = 0
        doc.cats["relocation"] = 0
        doc.cats["polish"] =0 
        doc.cats["police"] = 0
        doc.cats["Jewish"] = 0
        doc.cats["Nazi"] = 0 
        doc.cats["hospital"] = 0
        doc.cats["government"] = 0
        doc.cats["fear"] = 0
        doc.cats["hunger"] = 0
        doc.cats["family"] = 0
        doc.cats["camp"] = 0
        doc.cats["army"] = 0
        doc.cats["ghetto"] = 0
        doc.cats["religion"] = 0 
        doc.cats["shooting"] = 0
        doc.cats["food"] = 0
        doc.cats["aid"] = 0
        doc.cats["hiding"] = 0
        doc.cats["survive"] = 0
        doc.cats["sick"] = 0
        doc.cats["american"] = 0
        doc.cats["synagogue"] = 0
        doc.cats["buildings"] = 0
        doc.cats["prisoners"] = 0
        doc.cats["kill"] = 0
       
        if tag == "war":
            doc.cats["war"] = 1

        elif tag == "work":
            doc.cats["work"] = 1
        
        elif tag == "school":
            doc.cats["school"] = 1

        elif tag == "russian":
            doc.cats["russian"] = 1

        elif tag == "relocation":
            doc.cats["relocation"] = 1                    

        elif tag == "polish":
            doc.cats["polish"] = 1

        elif tag == "police":
            doc.cats["police"] = 1
                        
        elif tag == "Jewish":
            doc.cats["Jewish"] = 1

        elif tag == "Nazi":
            doc.cats["Nazi"] = 1

        elif tag == "hospital":
            doc.cats["hospital"] = 1
        
        elif tag == "government":
            doc.cats["government"] = 1

        elif tag == "fear":
            doc.cats["fear"] = 1

        elif tag == "hunger":
            doc.cats["hunger"] = 1                    

        elif tag == "family":
            doc.cats["family"] = 1

        elif tag == "camp":
            doc.cats["camp"] = 1
                        
        elif tag == "army":
            doc.cats["army"] = 1

        elif tag == "ghetto":
            doc.cats["ghetto"] = 1                    

        elif tag == "religion":
            doc.cats["religion"] = 1

        elif tag == "shooting":
            doc.cats["shooting"] = 1
                        
        elif tag == "food":
            doc.cats["food"] = 1

        elif tag == "aid":
            doc.cats["aid"] = 1

        elif tag == "hiding":
            doc.cats["hiding"] = 1
        
        elif tag == "survive":
            doc.cats["survive"] = 1

        elif tag == "sick":
            doc.cats["sick"] = 1

        elif tag == "american":
            doc.cats["american"] = 1                    

        elif tag == "synagogue":
            doc.cats["synagogue"] = 1

        elif tag == "buildings":
            doc.cats["buildings"] = 1
                        
        elif tag == "prisoners":
            doc.cats["prisoners"] = 1

        elif tag == "kill":
            doc.cats["kill"] = 1

        docs.append(doc)
    return (docs) 


def print_top_tags(tags: dict) -> None:

    NUMB_OF_TAGS = 3
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    for i in range(NUMB_OF_TAGS):
        pair = next(pair_iter)
        print(f"tag:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")
    



def test_model() -> None:

    TESTING_SAMPLES = 3

    nlp = spacy.load("model_output_exclusive/model-last")


    for tag in tags:
        print("\n===========================================================================\n")

        tag_file = open("./model_data/"+ tag + "/test.txt","r",encoding = "utf-8")
    
        print("TESTING " + tag.upper() + " CATEGORY\n")

        text = []
        for line in tag_file:
            text.append(line)
        print("\n")

        for i in range(TESTING_SAMPLES):
            print(text[i].strip())
            doc = nlp(text[i])
            print_top_tags(doc.cats)
            print("\n")
        tag_file.close()
    #text = "If I get trapped, then I wait there. Q: What else can you describe about conditions at that time? 7 A: Jewish people were very scared at that time. I think, or I heard that most of the bombardment at that time was directed to the Jewish quarter, most of the bombardment and I guess Jews were very much congregated in one area and the Germans were aware -- in fact they were aware of everything, but this in Warsaw. Q: Were you hiding in this Jewish area? A: Yes, I was hiding in the Jewish area wherever I could. Q: Do you have any remembrance of any Polish catholic people you knew at this time. Did your relationship with them change or did you separate? A: I think it was very much -- there were cold sufferers and they used to meet at the river if they get water, and it didn't make at that point in time, it didn't make any difference whether you were Jewish, Polish, catholic. At that point we were all Poles against the Germans. I want you to know the Jews were more interested to fight the Germans because they knew"
    # text = "Jewish people were very scared at that time. I think, or I heard that most of the bombardment at that time was directed to the Jewish quarter, most of the bombardment and I guess Jews were very much congregated in one area and the Germans were aware --"
    # doc = nlp(text)

    #print(doc.cats)

def top_tag(tags : dict) -> str:
    sorted_d = dict( sorted(tags.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)
    pair = next(pair_iter)
    #print(f"tag:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")
    return pair[0]




def display_matrix() -> None:


    PREDICTION_SAMPLES = 500
    true_values = []
    prediction_values = []
    line = []
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

    #print(true_values)
    #print(prediction_values)

    matrix = confusion_matrix(true_values,prediction_values,labels = tags)
    #print(matrix)
    create_heat_map(matrix)

def create_heat_map(matrix) -> None:

    #anotated_matrix = []
    anotated_matrix= matrix.tolist()
    matrix_text = [[str(y) for y in x] for x in anotated_matrix] 

    #set up figure 
    fig = ff.create_annotated_heatmap(anotated_matrix, x=tags, y=tags, 
    annotation_text=matrix_text, colorscale='Viridis')

    # add title
    fig.update_layout(title_text='<i><b>                                                                                          Confusion Matrix</b></i>',
                  #xaxis = dict(title='x'),
                  #yaxis = dict(title='x')
                 )

    # add custom xaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                        x=0.5,
                        y=-0.15,
                        showarrow=False,
                        text="Predicted value",
                        xref="paper",
                        yref="paper"))

    # add custom yaxis title
    fig.add_annotation(dict(font=dict(color="black",size=14),
                        x=-.12,
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
    fig.show()

    print("DONE CREATING CONFUSION MATRIX")



if __name__ == "__main__":


    try:
        if sys.argv[1] == "train":
            train_model()
        elif sys.argv[1] == "test":
            test_model()
        elif sys.argv[1] == "display":
            display_matrix()
    except IndexError:
        print("use \" python multilcass.py train\" to train a model or \" python multiclass.py test\" to test the model")