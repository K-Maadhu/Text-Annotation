#All common functions used in the Processing and Validation files are present in this program
#These are functions primarily used during the training and testing of the model

import spacy
import re
import pickle
import pandas as pd
from nltk.corpus import wordnet as wn
from spellchecker import SpellChecker
from tqdm import tqdm

tqdm.pandas()

stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
              "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
              "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
              "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
              "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
              "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
              "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
              "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
              "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
              "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "place", "places", "food",
              "service", "waiter", "water", "menu", "dish", "clean", "location", "parking", "table", "dinner", "cost", "bill",
              "ambiance", "bangalore", "glass", "upholstery", "vegetarian", "review", "weekend", "lights", "kids", "service",
              "party", "deal", "outing", "family", "friday", "saturday", "sunday", "zomato", "gold", "table", "months", "days",
              "atmosphere", "restaurant", "prices", "reviews", "weekends", "price", "expectations", "must", "meet", "heat", "cold",
              "hot", "cool", "taste", "tasty", "india", "indian", "north", "northern", "south", "southern"]

nlp = spacy.load('en')

spell = SpellChecker()
spell.word_frequency.load_text_file(r'Data\list_of_foods.txt')

pkl_file = open(r'Data\all_foods.pkl', 'rb')
all_foods = pickle.load(pkl_file)

user_foods = pd.read_csv(r'Data\User List.csv')
user_foods.drop(user_foods.columns[0], axis=1, inplace=True)
userfood_list = list(user_foods.query("Type == 'food'")['Word'])


def get_aspects(review):
    try:
        res = re.sub('[^a-zA-Z]+', ' ', review)
        doc = nlp(res)  ## Tokenize and extract grammatical components
        doc = [i.text for i in doc if
               i.text.lower() not in stop_words and i.pos_ == "NOUN"]  ## Remove common words and retain only nouns
        doc = list(map(lambda i: i.lower(), doc))  ## Normalize text to lower case
    except:
        print(review)
    return doc

spell_corrected = 0

def isFood(word):
    global spell_corrected
    type = 'not-food'
    if len(wn.synsets(word)) == 0:
        if word in all_foods:
            type = 'food'
            return (type)
        else:
            typo_corrected = spell.correction(word)
            spell_corrected += 1
            if len(wn.synsets(typo_corrected)) == 0:
                if typo_corrected in all_foods:
                    type = 'food'
                    return (type)
                else:
                    # print('e. '+word)
                    type = 'word-not-found'
                    return (type)
            else:
                for syns in wn.synsets(typo_corrected):
                    if (syns.lexname() == 'noun.food'):
                        type = 'food'
                        break
                return (type)
    else:
        for syns in wn.synsets(word):
            if (syns.lexname() == 'noun.food'):
                type = 'food'
                break
        return (type)


def set_labels(review_comm):
    label_text = []
    rev = re.sub('[^a-zA-Z]+', ' ', review_comm)
    for i in rev.split(' '):
        if i.lower() not in stop_words and (i.lower() in all_foods or i.lower() in userfood_list):
            label = 'F'
        else:
            label = 'I'
        if len(i) > 0:
            label_text.append((i, label))
    return label_text

#This code is from the sample CRF Suite package, and is used as delivered
def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]

    # Common features for all words
    features = [
        'bias',
        'word.lower=' + word.lower(),
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'word.isupper=%s' % word.isupper(),
        'word.istitle=%s' % word.istitle(),
        'word.isdigit=%s' % word.isdigit(),
        'postag=' + postag
    ]

    # Features for words that are not at the beginning of a document
    if i > 0:
        word1 = doc[i - 1][0]
        postag1 = doc[i - 1][1]
        features.extend([
            '-1:word.lower=' + word1.lower(),
            '-1:word.istitle=%s' % word1.istitle(),
            '-1:word.isupper=%s' % word1.isupper(),
            '-1:word.isdigit=%s' % word1.isdigit(),
            '-1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS')

    # Features for words that are not at the end of a document
    if i < len(doc) - 1:
        word1 = doc[i + 1][0]
        postag1 = doc[i + 1][1]
        features.extend([
            '+1:word.lower=' + word1.lower(),
            '+1:word.istitle=%s' % word1.istitle(),
            '+1:word.isupper=%s' % word1.isupper(),
            '+1:word.isdigit=%s' % word1.isdigit(),
            '+1:postag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS')

    return features

#Function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]

#Function for generating the list of labels for each document
def get_labels(doc):
    return [label for(token, postag, label) in doc]

def clean_comments(review_comm):
    clean_text = []
    rev = re.sub('[^a-zA-Z]+', ' ', review_comm)
    for i in rev.split(' '):
        if len(i) > 0:
            typo_corrected = spell.correction(i)
            clean_text.append(typo_corrected)
    return clean_text


def get_comments(file_name_or_comm, file=0):
    if file == 0:  # Single comment and not a file
        ret_comments = clean_comments(file_name_or_comm)
    else:
        read_comments = pd.read_csv('Data\\' + file_name_or_comm)
        #read_comments = pd.read_csv(r'\Data\Silbatti.csv')
        ret_comments = read_comments['Review'].head(100).progress_apply(clean_comments)
        ret_comments = ret_comments.tolist()
    return ret_comments

