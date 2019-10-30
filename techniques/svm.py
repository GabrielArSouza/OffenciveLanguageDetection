import load_dataset as dataset 
import tfidf 
import numpy as np 
import matplotlib.pyplot as plt

def lower_case (word_list):
    return [entry.lower() for entry in word_list]

def word_tokenize(phrase, stop_words):
    phrase_list = phrase.split()
    
    # remove stop words
    new_list = []
    for word in phrase_list:
        if word not in stop_words:
            new_list.append(word)
    return new_list

def preprocess ():
    positive, negative, stop_words = dataset.load()
    
    positive = lower_case(positive)
    negative = lower_case(negative)
    
    # create vectors for each message
    positive_vectors = [[]]
    negative_vectors = [[]]

    [positive_vectors.append(word_tokenize(msg, stop_words)) for msg in positive]
    [negative_vectors.append(word_tokenize(msg, stop_words)) for msg in negative]
    return positive_vectors, negative_vectors

def create_train_dataset (pos, neg):
    terms = {}
    for term in pos.keys():
        terms[term] = {}
    for term in neg.keys():
        terms[term] = {}

    dataset = {}
    
    pos_x = []
    pos_y = []
    neg_x = []
    neg_y = []

    for term in terms:
        x = 0.0
        y = 0.0
        if term in pos.keys():
            x = pos[term]
            pos_x.append(x)
            pos_y.append(neg[term] if term in neg.keys() else '0.0')
        if term in neg.keys():
            y = neg[term]
            neg_y.append(y)
            neg_x.append(pos[term] if term in pos.keys() else '0.0')
        dataset[term] = {'x' : x, 'y' : y}

    plt.figure(figsize=(8,6))
    plt.scatter(pos_x, pos_y, marker='+', color='green')
    plt.scatter(neg_x, neg_y, marker='_', color='red')
    plt.show()

    # define x as pos and y as neg

def train (positive, negative, alpha=0.0001, max_epochs=10000):
    size = 0
    if len(positive) < len(negative):
        size = len(positive)
    else:
        size = len(negative)

if __name__ == '__main__':
    positive, negative = preprocess()
    tf_pos = tfidf.tfidf(positive)
    tf_neg = tfidf.tfidf(negative)

    #print (tf_neg)
    create_train_dataset(tf_pos, tf_neg)

