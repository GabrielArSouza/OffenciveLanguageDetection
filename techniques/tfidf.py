import math

terms = {}
term_frequency = {}
inverse_frequency = {}

def tf ():
    total_terms = 0
    for value in terms.keys():
        total_terms += terms[value]

    global term_frequency
    for term in terms:
        term_frequency[term] = terms[term] / total_terms

def idf (list_documents):
    global inverse_frequency
    num_documents = len(list_documents)

    global terms
    for term in terms:
        # number of documents with term t        
        cont = 0
        for doc in list_documents:
            if term in doc:
                cont += 1
        inverse_frequency[term] = math.log10(num_documents/cont)
            

def add_term (term):
    global terms
    if term in terms:
        terms[term] = terms[term] + 1
    else:
        terms[term] = 1

def tfidf (list_documents):

    #print (len(list_documents))
    # populate the list of terms occurrences
    global terms
    terms = {}
    for document in list_documents:
        [add_term(term) for term in document] 
    
    tf()
    idf(list_documents)

    global term_frequency, inverse_frequency
    tfidf = {}
    for term in terms.keys():
        tfidf[term] = "{0:.6f}".format(term_frequency[term] * inverse_frequency[term])
    
    return tfidf

