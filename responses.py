# Finds Response

'''
Takes input from cwi.py and passes into model
Best response is gained
Response outputted to cwi.py for display
'''

# ---------------------------------------------------------------------------------------------------------------------
# Imports

import os
import pickle
import random
import json
import numpy
import nltk
from nltk.stem import WordNetLemmatizer
from keras.models import load_model

# ---------------------------------------------------------------------------------------------------------------------
# BOW Functions

def message_clean_up(message_text):
    '''
    Processing input string - tokenising and lemmatising
    '''

    message_words = nltk.word_tokenize(message_text)
    message_words = [lemmatiser.lemmatize(word) for word in message_words]
    return message_words

def bow(message_text, words):
    '''
    Bag of Words algorithm, creates a numpy binary array
        - if an input word matches the training data => 1
    '''

    message_words = message_clean_up(message_text)
    bag = [0] * len(words)
    
    # test each input word against every training word
    for m_word in message_words:
        for i, word in enumerate(words):
            if word == m_word:
                bag[i] = 1
    return numpy.array(bag)

# ---------------------------------------------------------------------------------------------------------------------
# Class Prediction + Response Retrieval Functions

def get_probabilities(message_text, words, model):
    '''
    Passes the bag of words into the model, gets probablilities of word classes
    Filters the probablilites to get probablitity and index
    '''

    bag_of_words = bow(message_text, words)
    prediction = model(numpy.array([bag_of_words]), training=False)[0] # returns an array of probabilities
    results = [[i, result] for i, result in enumerate(prediction) if result > ERROR_THRESHOLD] # filters insignificant results
    return results

def get_class(results, word_classes):
    '''
    Sorts results to get the top class prediction and class tag
    '''

    results.sort(key=lambda x:x[1], reverse=True) # sorts highest to lowest
    class_index = results[0][0]
    class_tag = word_classes[class_index]
    return class_tag

def get_response(class_tag, corpus):
    '''
    Gets a random response from within the selected class
    '''

    corpus_intents = corpus['intents']
    for i in corpus_intents:
        if i['tag'] == class_tag:
            chatbot_response = random.choice(i['responses'])
    return chatbot_response

# ---------------------------------------------------------------------------------------------------------------------
# Main Function

def responses_main(model_name, message_text):
    '''
    Main response function, calls other functions and loads necessary files
    Returns the ai response
    '''

    # loading files
    words = pickle.load(open(f'{current_path}/models/{model_name}_words.pkl', 'rb'))
    word_classes = pickle.load(open(f'{current_path}/models/{model_name}_classes.pkl', 'rb'))
    model = load_model(f'{current_path}/models/{model_name}_model.h5')
    corpus = json.loads(open(f'{current_path}/corpora/{model_name}.json').read())

    # returning a response
    results = get_probabilities(message_text, words, model)
    class_tag = get_class(results, word_classes)
    response = get_response(class_tag, corpus)
    return response

# ---------------------------------------------------------------------------------------------------------------------
# Globals

current_path = os.getcwd()
lemmatiser = WordNetLemmatizer()
ERROR_THRESHOLD = 0.1
