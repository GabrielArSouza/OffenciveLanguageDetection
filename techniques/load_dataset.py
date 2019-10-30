import json

# repository from train and test dataset
train = "../dataset/train/"
stop_words_repo = "../files/stop_words.in"

def read_stop_words ():
    stop_words = []
    with open(stop_words_repo, 'r') as fp:
        for line in fp:
            stop_words.append(line.rstrip('\n'))
    return stop_words

def load_messages ():
    positive_repo = train + "positive.txt"
    
    # read positive messages for offensive
    positive_messages = []
    with open(positive_repo, 'r') as fp:
        for line in fp:
            positive_messages.append(json.loads(line)['clean_message'])
    negative_repo = train + "negative.txt"
    
    # read negative messages for offensive
    negative_messages = []
    with open(negative_repo, 'r') as fp:
        for line in fp:
            negative_messages.append(json.loads(line)['clean_message'])
            
    return positive_messages, negative_messages

def load ():
    
    stop_words = read_stop_words()
    positive_messages, negative_messages = load_messages ()

    return positive_messages, negative_messages, stop_words