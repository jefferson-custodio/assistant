#%%
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

# things we need for Tensorflow
import json
import numpy as np

import pandas as pd
import random
from tensorflow.keras.models import model_from_json

# Opening JSON file
f = open('intents.json',)
  
# returns JSON object as 
# a dictionary
intents = json.load(f)

words = []
classes = []
documents = []
ignore_words = ['?']

# loop through each sentence in our intents patterns
for intent in intents['intents']:
    for pattern in intent['patterns']:
        # tokenize each word in the sentence
        w = nltk.word_tokenize(pattern, language='portuguese')
        # add to our words list
        words.extend(w)
        # add to documents in our corpus
        documents.append((w, intent['tag']))
        # add to our classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# stem and lower each word and remove duplicates
words = [stemmer.stem(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))
# sort classes
classes = sorted(list(set(classes)))



model_file = open('model.json', 'r')
network_structure = model_file.read()
model_file.close()

model = model_from_json(network_structure)
model.load_weights('model.h5')

def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [stemmer.stem(word.lower()) for word in sentence_words]
    return sentence_words
    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence
def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    
    return(np.array(bag))

# p = bow("Load blood pessure for patient", words)
# print (p)
# print (classes)

# # Use pickle to load in the pre-trained model
# global graph
# graph = tf.compat.v1.get_default_graph()

# with open(f'katana-assistant-model.pkl', 'rb') as f:
#     model = pickle.load(f)

def classify_local(sentence):
    ERROR_THRESHOLD = 0.60
    
    # generate probabilities from the model
    input_data = pd.DataFrame([bow(sentence, words)], dtype=float, index=['input'])
    results = model.predict([input_data])[0]
    # filter out predictions below a threshold, and provide intent index
    results = [[i,r] for i,r in enumerate(results) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({ "intent": classes[r[0]], "probability": str(r[1]) })
    # return tuple of intent and probability
    
    return return_list

def get_answer(sentence):
    list_of_intents = intents['intents']
    tag = 'noanswer'

    result_classify = classify_local(sentence)
    print(result_classify)

    if len(result_classify) > 0:
        tag = result_classify[0]['intent']
   
    for i in list_of_intents: 
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break

    return result


# running the chatbot
# while True:
message = input("\033[96m Diga: ")
answer = get_answer(message)
print('\033[92m -> Resposta: ' + answer + '\033[96m')

# %%
