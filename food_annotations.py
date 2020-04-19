import pycrfsuite
from Functions import word2features, clean_comments
import nltk

def extract_features(doc):
    print('======================Extracting features===================')
    return [word2features(doc, i) for i in range(len(doc))]

def get_annotations(doc):

    cleaned_input = clean_comments(doc)

    #Perform POS Tagging
    tagged = nltk.pos_tag(cleaned_input)
    print('======================Tokenizing complete===================')
    
    #Take the word and POS tag
    new_data=[]
    new_data.append([(pos) for w, pos in zip(cleaned_input, tagged)])

    new_X = [extract_features(doc) for doc in new_data]
    tagger = pycrfsuite.Tagger()
    
    print('======================Loading model===================')
    tagger.open(r'crf_menu.model')
    
    print('======================Predicting===================')
    y_pred = [tagger.tag(x_seq) for x_seq in new_X]
    
    html_resp = ''    
    
    i=0
    for word in cleaned_input:
        print(word + '-' + y_pred[0][i])
        if y_pred[0][i]=='F':
            word = '<u><b>' + word + '</b></u>'
        html_resp += word + " "
        i+=1
    return(html_resp)