import nltk
from tqdm import tqdm
import pycrfsuite
from Functions import *

#Program fails in the nltk.pos_tag function without one time download of this tagger.
#This is one time effort and can be commented after that.
#nltk.download('averaged_perceptron_tagger')


#This all files is a collection of 9 input files, leaving the remaininig 3 files for hold-out testing
comments = pd.read_csv(r'Data\all_files.csv')
print(comments.shape)

words = []
words = comments['Review'].apply(get_aspects)

user_words = []
for i in words:
    user_words += i

setofwords = set(user_words)
print(len(setofwords))
print(setofwords)


print(all_foods)

#% % time
userlist = []
for items in tqdm(setofwords):
    value = isFood(items)
    if value != 'not-food':
        userlist.append({'Word': items, 'Type': value})
print("Total spelling corrected words are %d" % spell_corrected)

userlist = pd.DataFrame(userlist)
userfood_list = list(user_foods.query("Type == 'food'")['Word'])

keywords_file = 'Data\\User List.csv'
file_obj = open(keywords_file, 'w')
userlist.to_csv(file_obj)
file_obj.close()

#% % time
labeled_list = comments['Review'].apply(set_labels)
labeled_list = labeled_list.tolist()

data = []
for i, doc in enumerate(labeled_list):
    # Obtain the list of tokens in the document
    tokens = [t for t, label in doc]

    # Perform POS Tagging
    tagged = nltk.pos_tag(tokens)

    # Take the word, POS tag and it's label
    data.append([(w, pos, label) for (w, label), (word, pos) in zip(doc, tagged)])


X = [extract_features(doc) for doc in data]
y = [get_labels(doc) for doc in data]

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

trainer = pycrfsuite.Trainer(verbose=True)

# Submit training data to the trainer
# for xseq, yseq in zip(X_train, y_train):
# trainer.append(xseq, yseq)
for xseq, yseq in zip(X, y):
    trainer.append(xseq, yseq)

# Set the parametrs for the model
trainer.set_params({
    # Coefficient for L1 penalty
    'c1': 0.1,

    # Coefficient for L2 penalty
    'c2': 0.01,

    # Maximum number of iterations
    'max_iterations': 200,

    # Whether to include transitions that are possible, but not observed
    'feature.possible_transitions': True
})

# Provide a file name as a parameter to the train function, such that
# the model will be saved to the file when training is finished
trainer.train('crf_menu.model')

