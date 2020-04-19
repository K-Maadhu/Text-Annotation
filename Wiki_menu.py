from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
import spacy
import pickle

#Load NLP for the English language
nlp = spacy.load('en')

stop_words=["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself",
            "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself",
            "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these",
            "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do",
            "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
            "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before",
            "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
            "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than",
            "too", "very", "s", "t", "can", "will", "just", "don", "should", "now", "place", "places", "food", "service",
           "waiter", "water", "menu", "dish", "clean", "location", "parking", "table", "dinner", "cost", "bill", "ambiance",
            "bangalore", "glass", "upholstery", "vegetarian", "review", "weekend", "lights", "kids", "service", "party", "deal",
           "outing", "family", "friday", "saturday", "sunday", "zomato", "gold", "table", "months", "days", "atmosphere",
            "restaurant", "prices", "reviews", "weekends", "price", "expectations", '/', '*', 'tamil', 'nadu', 'kerala',
            'karnataka', 'andhra', 'pradesh']

def get_items(descr):
 doc=nlp(descr) ## Tokenize and extract grammatical components
 doc=[i.text for i in doc if i.text.lower() not in stop_words and i.pos_=="NOUN"] ## Remove common words and retain only nouns
 doc=list(map(lambda i: i.lower(),doc)) ## Normalize text to lower case
 return doc

#Read Wikipedia page to build corpus of India food items
wiki = 'https://en.wikipedia.org/wiki/List_of_Indian_dishes'
page = requests.get(wiki)
contents = bs(page.text, "html.parser")

get_tables = pd.read_html(wiki)

#Read table 3 of the page to get the North Indian dishes info
north_dishes = list(get_tables[3][0])
north_dishes.remove('Name')
print(north_dishes)

north_dishes = set(map(lambda i: i.lower(), north_dishes))
menu = list(north_dishes)

each_word = []
remove = ['(', ')']
for i in north_dishes:
    for j in i.split(' '):
        if j not in stop_words:
            for k in remove:
                j = j.replace(k, '')
            each_word.append(j)

each_word = list(set(each_word))
print(each_word)
print(menu)

north_desc = get_tables[3][2]
north_desc = north_desc.dropna()

north_clean_desc = north_desc.apply(get_items)
north_clean_desc = north_clean_desc[1:]
print(north_clean_desc)

food_item = []
for i in north_clean_desc:
    food_item += i

northfoods = menu+each_word+food_item
print(northfoods)


#Read table 4 of the page to get the South Indian dishes info
south_dishes = list(get_tables[4][0])
south_dishes.remove('Name')

south_dishes = set(map(lambda i: i.lower(), south_dishes))
south_menu = list(south_dishes)
print(south_menu)

remove = ['(', ')', ',']
each_words = []
south_each_word = []
for i in south_dishes:
    for j in i.split(' '):
        if j.strip() not in stop_words:
            for k in remove:
                j = j.replace(k, ' ')
            each_words.append(j)
for i in each_words:
    for j in i.split(' '):
        if j.strip() not in stop_words:
            south_each_word.append(j)
south_each_word = list(set(south_each_word))
print(south_each_word)

south_desc = get_tables[4][2]
south_desc = south_desc.dropna()
south_clean_desc = south_desc.apply(get_items)
south_clean_desc = south_clean_desc[1:]

south_food_item = []
for i in south_clean_desc:
    south_food_item += i
print(south_food_item)

southfoods = south_menu + south_each_word + south_food_item
print(southfoods)

#Add both the sets to create one comprehensive collection of menu items
all_foods = set(northfoods + southfoods)
print(all_foods)

#Create a pickle object of this corpus
output = open(r'Data\all_foods.pkl', 'wb')
pickle.dump(all_foods, output)
output.close()