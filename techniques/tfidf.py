terms = {}
term_frequency = {}
inverse_frequency = {}
tfidf = {}

def tf (document):
    occurrences = {}
    total_words = 0
    
    # calculate occurrences words in document
    for word in document:
        total_words += 1
        if word in occurrences:
            occurrences[word] = occurrences[word]+1
        else:
            occurrences[word] = 1
    tf = {}
    for word in occurrences.keys():
        tf[word] = occurrences[word] / total_words
    
    return tf


def idf (list_words):
    pass

def add_term (term):
    global terms
    if term in terms:
        terms[term] = terms[term] + 1
    else:
        terms[term] = 1

def tfidf (list_documents):

    # populate the list of terms occurrences
    for document in list_documents:
        [add_term(term) for term in document] 
        print (tf(document))  
    
