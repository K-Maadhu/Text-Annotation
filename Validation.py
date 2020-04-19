#Run the program for the remaining 3 files using the CRF_Menu model
from Functions import *
import pycrfsuite
import pandas as pd
import nltk
import numpy as np
from sklearn.metrics import classification_report


# %%time
new_comments = []
new_comments = get_comments('Silbatti.csv', 1)

# %%time
same_comments = pd.read_csv('Data\Silbatti.csv')
y_actuals = same_comments['Review'].head(100).progress_apply(set_labels)
y_actuals = y_actuals.tolist()

new_data = []
for i, doc in enumerate(new_comments):
    # Obtain the list of tokens in the document
    tokens = [word for word in doc]

    # Perform POS Tagging
    tagged = nltk.pos_tag(tokens)

    # Take the word and POS tag
    new_data.append([(pos) for w, pos in zip(tokens, tagged)])

print(new_data[0])

# def extract_features(doc):
#     return [word2features(doc, i) for i in range(len(doc))]


new_X = [extract_features(doc) for doc in new_data]

tagger = pycrfsuite.Tagger()
tagger.open('crf_menu.model')
y_pred = [tagger.tag(x_seq) for x_seq in new_X]

comment_id = 1
for i in range(len(new_X[comment_id])):
    actual_label = str(y_actuals[comment_id][i][1])
    print(new_comments[comment_id][i] + ' ' + y_pred[comment_id][i] + ' ' + actual_label)

labels = {'F': 1, 'I': 0}

# Convert the sequences of tags into a 1-dimensional array
predictions = np.array([labels[tag] for row in y_pred for tag in row])
truths = np.array([labels[act_label[1]] for row in y_actuals for act_label in row])

print('Total predicted food words are %d' % (np.sum(predictions)))
print('Total actual food words are %d' % (np.sum(truths)))

for i in range(len(new_X)):
    for j in range(len(new_X[i])):
        actual_label = str(y_actuals[i][j][1])
        if y_pred[i][j] != actual_label:
            print(new_comments[i][j] + ' ' + y_pred[i][j] + ' ' + actual_label)

# Print out the classification report
print(classification_report(truths, predictions, target_names=["I", "F"]))

predicted_food = []
for i in range(len(new_X)):
    for j in range(len(new_X[i])):
        if y_pred[i][j] == 'F':
            predicted_food.append(new_comments[i][j].lower())

predicted_set = set(predicted_food)
collate_list = []
for i in predicted_set:
    collate_list.append({'Word': i, 'Count': predicted_food.count(i)})
collate_list = pd.DataFrame(collate_list)
print(collate_list.sort_values(['Count'], ascending=False))