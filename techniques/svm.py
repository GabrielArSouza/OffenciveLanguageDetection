import load_dataset as dataset 
import tfidf 

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
    [negative_vectors.append(word_tokenize(msg, stop_words)) for msg in positive]
    return positive_vectors, negative_vectors
    
if __name__ == '__main__':
    positive, _ = preprocess()
    tfidf.tfidf(positive)
