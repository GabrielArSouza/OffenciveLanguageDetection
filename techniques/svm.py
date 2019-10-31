import load_dataset as dataset 
import tfidf 
import numpy as np 
import matplotlib.pyplot as plt

bag_of_words = {}
total_positive_words = 0
total_negative_words = 0

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

# construct bag of words 
def create_bag_of_words (pos, neg):
    global bag_of_words
    global total_positive_words
    global total_negative_words

    for elem in pos:
        for term in elem:
            total_positive_words += 1
            if term not in bag_of_words.keys():
                bag_of_words[term] = {'offensive' : 1, 'neither' : 0 }
            else:
                bag_of_words[term]['offensive'] = bag_of_words[term]['offensive'] + 1

    for elem in neg:
        for term in elem:
            total_negative_words += 1
            if term not in bag_of_words.keys():
                bag_of_words[term] = {'offensive' : 0, 'neither' : 1}
            else:
                bag_of_words[term]['neither'] = bag_of_words[term]['neither'] + 1
        
    return bag_of_words, total_positive_words, total_negative_words

def score_list_words (list_words):
    global bag_of_words, total_negative_words, total_positive_words
    print (list_words, len(list_words))
    if (len(list_words) < 1): return 0, 0
    offensive_score = 0
    neither_score = 0

    for word in list_words:
        offensive_score += (bag_of_words[word]['offensive']/total_positive_words)
        neither_score += (bag_of_words[word]['neither']/total_negative_words)
    
    offensive_score = offensive_score / len(list_words)
    neither_score = neither_score / len(list_words)

    return offensive_score, neither_score

def create_dataset (positive, negative):
    pos_x = []
    pos_y = []
    neg_x = []
    neg_y = []

    for pos in positive:
        p, n = score_list_words(pos)
        pos_x.append(p)
        pos_y.append(n) 
    
    for neg in negative:
        p, n = score_list_words(neg)
        neg_x.append(p)
        neg_y.append(n)

    plt.figure(figsize=(8,6))
    plt.scatter(pos_x,pos_y,marker='+',color='green')
    plt.scatter(neg_x,neg_y,marker='_',color='red')
    plt.show()

def train (dataset, alpha=0.0001, max_epochs=10000):
    pass

if __name__ == '__main__':
    positive, negative = preprocess()
    bag_of_words, total_positive, total_negative = create_bag_of_words(positive, negative)
    create_dataset(positive, negative)



