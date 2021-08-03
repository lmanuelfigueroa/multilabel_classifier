import sys
import spacy
from spacy.tokens  import DocBin
import random
import operator

def train_model() -> None:
    print("Training Model ....")

    nlp = spacy.blank("en")
    
    training_data = []
    validate_data = []
    
    labels = ["work","war","school"]
    # ,"russian","relocation","polish","police","Jewish","Nazi","hospital","government",
    # "fear","hunger","family","camp","army","ghetto","religion","shooting","food","aid","hiding","survive","sick","american",
    # "synagogue","buildings","prisoners","kill"]

   
    # creating the training samples for model with labels
    for label in labels:
        
        file = open("model_data/"+ label +"/train.txt","r",encoding = "utf-8")

        for line in file:
            training_data.append((line,label))
        file.close()

    
    #training_data = random.sample(training_data,len(training_data))

    #creating the valid samples for model with labels

    for label in labels:
        file = open("model_data/" + label + "/valid.txt","r",encoding = "utf-8")

        for line in file:
            validate_data.append((line,label))
        file.close()


    #validate_data = random.sample(validate_data,len(validate_data))
    
    #num_texts = 400

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
    for doc, label in nlp.pipe(data, as_tuples=True):

        #doc.cats["human_rights"] = 0
        doc.cats["war"] = 0
        doc.cats["work"] = 0
        doc.cats["school"] = 0
        # doc.cats["russian"] = 0
        # doc.cats["relocation"] = 0
        # doc.cats["polish"] =0 
        # doc.cats["police"] = 0
        # doc.cats["Jewish"] = 0
        # doc.cats["Nazi"] = 0 
        # doc.cats["hospital"] = 0
        # doc.cats["government"] = 0
        # doc.cats["fear"] = 0
        # doc.cats["hunger"] = 0
        # doc.cats["family"] = 0
        # doc.cats["camp"] = 0
        # doc.cats["army"] = 0
        # doc.cats["ghetto"] = 0
        # doc.cats["religion"] = 0 
        # doc.cats["shooting"] = 0
        # doc.cats["food"] = 0
        # doc.cats["aid"] = 0
        # doc.cats["hiding"] = 0
        # doc.cats["survive"] = 0
        # doc.cats["sick"] = 0
        # doc.cats["american"] = 0
        # doc.cats["synagogue"] = 0
        # doc.cats["buildings"] = 0
        # doc.cats["prisoners"] = 0
        # doc.cats["kill"] = 0
       

        # if label == "human_rights":
        #     doc.cats["human_rights"] = 1

        if label == "war":
            doc.cats["war"] = 1

        elif label == "work":
            doc.cats["work"] = 1
        
        elif label == "school":
            doc.cats["school"] = 1

        # elif label == "russian":
        #     doc.cats["russian"] = 1

        # elif label == "relocation":
        #     doc.cats["relocation"] = 1                    

        # elif label == "polish":
        #     doc.cats["polish"] = 1

        # elif label == "police":
        #     doc.cats["police"] = 1
                        
        # elif label == "Jewish":
        #     doc.cats["Jewish"] = 1

        # elif label == "Nazi":
        #     doc.cats["Nazi"] = 1

        # elif label == "hospital":
        #     doc.cats["hospital"] = 1
        
        # elif label == "government":
        #     doc.cats["government"] = 1

        # elif label == "fear":
        #     doc.cats["fear"] = 1

        # elif label == "hunger":
        #     doc.cats["hunger"] = 1                    

        # elif label == "family":
        #     doc.cats["family"] = 1

        # elif label == "camp":
        #     doc.cats["camp"] = 1
                        
        # elif label == "army":
        #     doc.cats["army"] = 1

        # elif label == "ghetto":
        #     doc.cats["ghetto"] = 1                    

        # elif label == "religion":
        #     doc.cats["religion"] = 1

        # elif label == "shooting":
        #     doc.cats["shooting"] = 1
                        
        # elif label == "food":
        #     doc.cats["food"] = 1

        # elif label == "aid":
        #     doc.cats["aid"] = 1

        # elif label == "hiding":
        #     doc.cats["hiding"] = 1
        
        # elif label == "survive":
        #     doc.cats["survive"] = 1

        # elif label == "sick":
        #     doc.cats["sick"] = 1

        # elif label == "american":
        #     doc.cats["american"] = 1                    

        # elif label == "synagogue":
        #     doc.cats["synagogue"] = 1

        # elif label == "buildings":
        #     doc.cats["buildings"] = 1
                        
        # elif label == "prisoners":
        #     doc.cats["prisoners"] = 1

        # elif label == "kill":
        #     doc.cats["kill"] = 1

        docs.append(doc)
    return (docs) 


def print_top_labels(labels: dict) -> None:

    NUMB_OF_LABELS = 3
    sorted_d = dict( sorted(labels.items(), key=operator.itemgetter(1),reverse=True))
    dict_pairs = sorted_d.items()
    pair_iter =  iter(dict_pairs)

    for i in range(NUMB_OF_LABELS):
        pair = next(pair_iter)
        print(f"Label:{pair[0]}\t Percentage: {round(pair[1]*100,2)}%")
    



def test_model() -> None:

    TESTING_SAMPLES = 3

    nlp = spacy.load("model_output/model-last")

    # testing_tags = ["Nazi","hospital","government",
    # "fear","hunger","family","camp","army"]

    # testing_tags2 = ["ghetto","religion","shooting","food","aid","hiding","survive","sick","american",
    # "synagogue","buildings","prisoners","kill"]

    tags = ["work","war","school"]
    # ,"russian","relocation","polish","police","Jewish","Nazi","hospital","government",
    # "fear","hunger","family","camp","army","ghetto","religion","shooting","food","aid","hiding","survive","sick","american",
    # "synagogue","buildings","prisoners","kill"]

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
            print_top_labels(doc.cats)
            print("\n")
        tag_file.close()
    #text = "If I get trapped, then I wait there. Q: What else can you describe about conditions at that time? 7 A: Jewish people were very scared at that time. I think, or I heard that most of the bombardment at that time was directed to the Jewish quarter, most of the bombardment and I guess Jews were very much congregated in one area and the Germans were aware -- in fact they were aware of everything, but this in Warsaw. Q: Were you hiding in this Jewish area? A: Yes, I was hiding in the Jewish area wherever I could. Q: Do you have any remembrance of any Polish catholic people you knew at this time. Did your relationship with them change or did you separate? A: I think it was very much -- there were cold sufferers and they used to meet at the river if they get water, and it didn't make at that point in time, it didn't make any difference whether you were Jewish, Polish, catholic. At that point we were all Poles against the Germans. I want you to know the Jews were more interested to fight the Germans because they knew"
    # text = "Jewish people were very scared at that time. I think, or I heard that most of the bombardment at that time was directed to the Jewish quarter, most of the bombardment and I guess Jews were very much congregated in one area and the Germans were aware --"
    # doc = nlp(text)

    #print(doc.cats)


if __name__ == "__main__":


    try:
        if sys.argv[1] == "train":
            train_model()
        elif sys.argv[1] == "test":
            test_model()
    except IndexError:
        print("use \" python multilcass.py train\" to train a model or \" python multiclass.py test\" to test the model")