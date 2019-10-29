import json, math
import load_dataset as dataset
import results

# repository from train and test dataset
train = "../dataset/train/"
test  = "../dataset/test/"
stop_words_repo = "../files/stop_words.in"

positive_messages = []
negative_messages = []
stop_words = []

def save_words ():
    classifier_table = {}
    total_offensive_words = 0
    total_normal_words = 0
 
    global stop_words
    global positive_messages
    for msg in positive_messages:
        words = msg.split()
        for word in words:
            if (word not in stop_words):
                total_offensive_words = total_offensive_words + 1

                if (word in classifier_table):
                    tmp = classifier_table[word]
                    tmp['offensive'] = tmp['offensive'] + 1
                    classifier_table[word] = tmp 
                else:
                    classifier_table[word] = {'offensive' : 1, 'normal': 0}

    global negative_messages
    for msg in negative_messages:
        words = msg.split()
        for word in words:
            if (word not in stop_words):
                total_normal_words = total_normal_words + 1
                if (word in classifier_table):
                    tmp = classifier_table[word]
                    tmp['normal'] = tmp['normal'] + 1
                    classifier_table[word] = tmp 
                else:
                    classifier_table[word] = {'offensive' : 0, 'normal': 1}
    return classifier_table, total_normal_words, total_offensive_words

def train_naive_bayes ():
    global positive_messages, negative_messages, stop_words
    positive_messages, negative_messages, stop_words = dataset.load()
    
    return save_words()

# return 1 if offensive, 2 otherwise
def classifier_message (classifier_table, total_normal_words, total_offensive_words, p, m, msg):
    total_words = total_normal_words + total_offensive_words
    offensive_score = math.log10(total_offensive_words/total_words)
    normal_score = math.log10(total_normal_words/total_words)

    words = msg.split()
    occur_offensive = 0
    occur_normal = 0
    
    global stop_words
    for word in words:
        if (word in stop_words): continue
        elif (word in classifier_table):
            occur_offensive = classifier_table[word]['offensive']
            occur_normal = classifier_table[word]['normal']
        else:
            occur_offensive = 0
            occur_normal = 0

        offensive_score = offensive_score + math.log10((occur_offensive + m*p)/(total_offensive_words + m))
        normal_score = normal_score + math.log10((occur_normal + m*p)/(total_normal_words + m))

    if (offensive_score >= normal_score):
        return 1
    else: return 2

def run ():
    classifier_table, total_normal_words, total_offensive_words = train_naive_bayes()

    tp = 0
    tn = 0
    fp = 0
    fn = 0

    p = 1
    m = 0.5

    with open("../dataset/test/positive.txt", 'r') as file_:
        for line in file_:
            msg = json.loads(line)['clean_message']
            c = classifier_message(classifier_table, total_normal_words, total_offensive_words, p, m, msg)
            if (c == 1): 
                tp = tp + 1
            else: 
                fn = fn + 1

    with open("../dataset/test/negative.txt", 'r') as file_:
        for line in file_:
            msg = json.loads(line)['clean_message']
            c = classifier_message(classifier_table, total_normal_words, total_offensive_words, p, m, msg)
            if (c == 2): 
                tn = tn + 1
            else: 
                fp = fp + 1

    results.print_results(tp,tn,fp,fn)

run()