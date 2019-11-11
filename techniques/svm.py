import load_dataset as loader 
import results
import tfidf 
import numpy as np 
import matplotlib.pyplot as plt

from sklearn.utils import shuffle

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

def preprocess (value="TRAIN"):

    positive, negative, stop_words = loader.load(value)
    
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
        

def score_list_words (list_words):
    global bag_of_words, total_negative_words, total_positive_words

    if (len(list_words) < 1): return 0, 0
    offensive_score = 0
    neither_score = 0

    for word in list_words:
        if word in bag_of_words.keys():
            offensive_score += (bag_of_words[word]['offensive']/total_positive_words)
            neither_score += (bag_of_words[word]['neither']/total_negative_words)
        else: continue

    offensive_score = offensive_score / len(list_words)
    neither_score = neither_score / len(list_words)

    return offensive_score, neither_score

def create_dataset (positive, negative):
    
    new_pos = []
    new_neg = [] 

    for pos in positive:
        p, n = score_list_words(pos)
        new_pos.append([p, n]) 
    
    for neg in negative:
        p, n = score_list_words(neg)
        new_neg.append([p, n])

    return new_pos, new_neg

    # plt.figure(figsize=(8,6))
    # plt.scatter(pos_x,pos_y,marker='+',color='green')
    # plt.scatter(neg_x,neg_y,marker='_',color='red')
    # plt.show()

def train (dataset, classes, max_epochs=500, alpha=0.0001):
    dataset_size = len(dataset)
    
    dataset_train_vector = np.array(dataset)
    classes_train_vector = np.array(classes)

    # transform classes in a vector
    classes_train_vector = classes_train_vector.reshape(dataset_size, 1)

    train_positive_feature = dataset_train_vector[:,0]
    train_negative_feature = dataset_train_vector[:,1]

    # transform features in vectors
    train_positive_feature = train_positive_feature.reshape(dataset_size, 1)
    train_negative_feature = train_negative_feature.reshape(dataset_size, 1)

    w_pos = np.zeros((dataset_size, 1))
    w_neg = np.zeros((dataset_size, 1))

    epochs = 1 
    while (epochs < max_epochs):
        value = w_pos * train_positive_feature + w_neg * train_negative_feature
        production = value * classes_train_vector
        print("epochs:", epochs)

        count = 0
        lambda_ = 1.0 / epochs  
        # adjust weights
        for val in production:
            if (val >= 1):
                cost = 0
                w_pos = w_pos - alpha * (2 * lambda_ * w_pos)
                w_neg = w_neg - alpha * (2 * lambda_ * w_neg)
            else:
                cost = 1 - val
                w_pos = w_pos + alpha * (train_positive_feature[count] * classes_train_vector[count] - 2 * lambda_ * w_pos)
                w_neg = w_neg + alpha * (train_negative_feature[count] * classes_train_vector[count] - 2 * lambda_ * w_neg)
            count += 1
        epochs += 1

    return w_pos, w_neg

def compute_metrics(real, predict):
    size_ = len(real)
    
    fp = 0
    fn = 0
    tp = 0
    tn = 0 

    for i in range(size_):
        if real[i] == -1 and predict[i] == -1:
            tp += 1
        elif real[i] == -1 and predict[i] == 1:
            fn += 1
        elif real[i] == 1 and predict[i] == 1:
            tn += 1
        elif real[i] == 1 and predict[i] == -1:
            fp += 1

    results.print_results (tp, tn, fp, fn)
 
def test (w_pos, w_neg, size_dataset_train):
    positive, negative = preprocess("TEST")
    positive, negative = create_dataset(positive, negative)

    print ("w_pos:", w_pos)
    print ("w_neg:", w_neg)

    # create vector of results and dataset
    dataset = []
    classes = []

    for val in positive:
        dataset.append(val)
        classes.append(-1)
    
    for val in negative:
        dataset.append(val)
        classes.append(1)
    
    size_dataset_test = len(dataset)

    dataset_test_vector = np.array(dataset)
    classes_test_vector = np.array(classes)

    # transform classes in a vector
    classes_test_vector = classes_test_vector.reshape(size_dataset_test, 1)

    ## Clip the weights 
    index = list(range(size_dataset_test, size_dataset_train))
    w_pos = np.delete(w_pos,index)
    w_neg = np.delete(w_neg,index)

    w_pos = w_pos.reshape(size_dataset_test, 1)
    w_neg = w_neg.reshape(size_dataset_test, 1)

    ## Extract the test data features 
    test_positive_feature = dataset_test_vector[:,0]
    test_negative_feature = dataset_test_vector[:,1]

    test_positive_feature = test_positive_feature.reshape(size_dataset_test, 1)
    test_negative_feature = test_negative_feature.reshape(size_dataset_test, 1)

    ## predict
    y_pred = w_pos * test_positive_feature + w_neg * test_negative_feature
  
    predictions = []
    for value in y_pred:
        if (val[0] > 1):
            predictions.append(1)
        else:
            predictions.append(-1)

    compute_metrics(classes_test_vector, predictions)

def run ():
    positive, negative = preprocess()       # get dataset
    create_bag_of_words(positive, negative) # create bag of words
    positive, negative = create_dataset(positive, negative) # convert all text in a numeric value

    # create vector of results and dataset
    dataset = []
    classes = []

    for val in positive:
        dataset.append(val)
        classes.append(-1)
    
    for val in negative:
        dataset.append(val)
        classes.append(1)
   
    dataset, classes = shuffle(dataset, classes)
    w_pos, w_neg = train(dataset, classes, max_epochs=100)
    test(w_pos, w_neg, len(dataset))


if __name__ == '__main__':
    
    positive, negative = preprocess()       # get dataset
    create_bag_of_words(positive, negative) # create bag of words
    positive, negative = create_dataset(positive, negative) # convert all text in a numeric value

    # create vector of results and dataset
    dataset = []
    classes = []

    for val in positive:
        dataset.append(val)
        classes.append(-1)
    
    for val in negative:
        dataset.append(val)
        classes.append(1)
   
    dataset, classes = shuffle(dataset, classes)
    w_pos, w_neg = train(dataset, classes, max_epochs=500)
    test(w_pos, w_neg, len(dataset))

    
