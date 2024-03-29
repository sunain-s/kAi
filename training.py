# Training the Neural Network

'''
Creates the models based on the corpora
Runs only if models don't exist
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
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.optimizers import SGD

# ---------------------------------------------------------------------------------------------------------------------
# Model Creation Functions

def create_training_data(word_set, word_classes_set, documents, corpus_name):
    '''
    Creates an array of data from a corpus, that matches the input data against the expected output
    - this is used to determine how well the model is working, and to form and optimise the loss function
    '''

    training_data = []
    output_layer_empty = [0] * len(word_classes_set) # output layer indicates which class the input belongs to
    
    # iterating through each document to create a set of training data
    for doc in documents:
        input_data = []
        doc_words = doc[0]
        doc_words = [lemmatiser.lemmatize(str(word).lower()) for word in doc_words]

        # matches lemmatised set of words against original tokenised pattern words to create a binary list
        for word in word_set:
            if word in doc_words:
                input_data.append(1)
            else:
                input_data.append(0)
        
        # correct output is the word class (doc[1]), creates an array of inputs that can be fed into the model
        output_layer = list(output_layer_empty)
        output_layer[list(word_classes_set).index(doc[1])] = 1 
        training_data.append([input_data, output_layer]) 
    create_model(training_data, corpus_name)

def create_model(training_data_arr, corpus_name):
    '''
    Using TensorFlow creates a Seq2Seq model that trains using the data formed in create_training_data()
    - model has nodes 256-128-128-4 with 0.2 Dropout between each layer
    - utilises Stochastic Gradient Descent, Categorical Crossentropy loss function, ReLU and Softmax functions to get probabilities
    - runs for 200 generations
    '''

    # randomising data and converting to numpy array as required by TensorFlow
    random.shuffle(training_data_arr)
    training_data_arr = numpy.array(training_data_arr)
    input_train = list(training_data_arr[:, 0])
    output_train = list(training_data_arr[:, 1])

    # creating the model with the specified layers 
    model = Sequential()
    model.add(Dense(256, input_shape=(len(input_train[0]),), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(128, input_shape=(1,), activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(len(output_train[0]), activation='softmax'))

    # optimisation and loss function implementation for machine learning
    sgd = SGD(learning_rate=0.01, momentum=0.5, nesterov=True)
    model.compile(loss='categorical_crossentropy', optimizer=sgd, weighted_metrics=['accuracy'])
    model_owr = model.fit(numpy.array(input_train), numpy.array(output_train), epochs=200, batch_size=5, verbose=1)
    model.save(f'models/{corpus_name}_model.h5', model_owr)
    
# ---------------------------------------------------------------------------------------------------------------------
# Data Functions

def get_corpus_data(corpus_file):
    '''
    Extracts all the corpus data from a given JSON file and stores them in lists
    - gets pattern words, class tag names and documents (word-class pairs)
    '''

    words = []
    word_classes = []
    docs = []
    corpus = json.loads(open(f'{current_path}/corpora/{corpus_file}').read()) # reading the given corpus, turns it into a python dictionary

    # loops through each word class and obtains data
    for intent in corpus['intents']:
        for pattern in intent['patterns']:
            pattern_words = nltk.word_tokenize(pattern) # splits strings into words
            words.extend(pattern_words)
            docs.append((pattern_words, intent['tag']))
            if intent['tag'] not in word_classes:
                word_classes.append(intent['tag'])
    save_data(words, word_classes, docs, corpus_file)
    
def save_data(words_lst, word_classes_lst, docs, corpus_file):
    '''
    Saves the pattern words and classes from the corpus as alphabetical sets
    File format .pkl, to preserve the nature of the data (sets)
    '''

    corpus_name = str(corpus_file).strip('.json')
    words = [lemmatiser.lemmatize(str(word).lower()) for word in words_lst if word not in ignore_chrs] # ignores punctuation
    words = sorted(set(words))
    word_classes = sorted(set(word_classes_lst))
    pickle.dump(words, open(f'models/{corpus_name}_words.pkl', 'wb'))
    pickle.dump(word_classes, open(f'models/{corpus_name}_classes.pkl', 'wb'))
    create_training_data(words, word_classes, docs, corpus_name)
    
# ---------------------------------------------------------------------------------------------------------------------
# Main Function

def training_main():
    '''
    Main function of the training file, runs functions upon every JSON corpus in the file directory
    '''

    for i in range(len(corpora)):
        get_corpus_data(corpora[i])

# ---------------------------------------------------------------------------------------------------------------------
# Globals

current_path = os.getcwd()
corpora = [file for file in os.listdir(f'{current_path}/corpora/') if file.endswith('.json')]
lemmatiser = WordNetLemmatizer()
ignore_chrs = ['?', '!', '.', ',', "'", '"', '/', '£', '$', 
                '%', '^', '&', '*', '@', ':', ';', '#', '~', 
                '|', '<', '>', '{', '}', '_', '-', '+', '='
]

# ---------------------------------------------------------------------------------------------------------------------
# Runs File

if __name__ == '__main__':
    training_main()
