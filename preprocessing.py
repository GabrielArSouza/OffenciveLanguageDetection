import csv, sys, re, json
import random

FILENAME = "dataset/labeled_data.csv"

def clean_message (message):
    tmp = re.sub(r'RT @[a-zA-Z0-9_]*','<retweet>', message) # remove retweets
    tmp = re.sub(r'@[a-zA-Z0-9_]*',' <user>', tmp)            # remove users
    tmp = re.sub(r'&#[0-9]*;', ' <emoji>', tmp)               # remove emojis
    tmp = re.sub(r'#[0-9a-zA-Z]+',' <hastag>', tmp)          # remove hashtags
    tmp = re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', '<url>', tmp)
    tmp = re.sub(r'[^\w\s]',' ', tmp)                         # remove punctuation
    return tmp.lower() # lower case

def get_urls (message):
    pattern = re.compile('(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})')
    return pattern.findall(message)

def get_users (message):
    pattern = re.compile('@[a-zA-Z0-9_]*')
    return pattern.findall(message)

def get_retweets (message):
    pattern = re.compile('RT @[a-zA-Z0-9_]*')
    return pattern.findall(message)

def get_emojis (message):
    pattern = re.compile('&#[0-9]*;')
    return pattern.findall(message)

def get_hashtags (message):
    # remove emojis 
    tmp = re.sub(r'&#[0-9]*;', '', message)  
    pattern = re.compile('#[0-9a-zA-Z]+')
    return pattern.findall(tmp)

# Separate a dataset in a train set and test set
def separate_dataset(dataset, train, test):
    number_of_classes = len(dataset)
    
    # select the min size
    min_size = sys.maxsize
    for elem in dataset:
        if (len(elem) < min_size):
            min_size = len(elem)
    
    # create a selective dataset - select a random number
    # of elem for either class with the same size
    random.seed(1)
    new_dataset = []
    for elem in dataset:
        new_dataset.append(random.sample(elem, min_size))
    
    train_size = int(train * min_size)
    test_size = int(test * min_size)
    
    new_dataset_train = []
    new_dataset_test = []

    for elem in new_dataset:
        print (len(elem))
        new_dataset_train.append(elem[:train_size])
        new_dataset_test.append(elem[train_size:])
    
    return new_dataset_train, new_dataset_test

def read_csv_file ():
    
    dataset = [[], [], []]

    # read csv file
    global FILENAME
    with open(FILENAME) as csvfile:
        readed_csv = csv.reader(csvfile, delimiter=',')
        
        for row in readed_csv:
            data = {}
            data['message'] = row[-1].encode('ascii', 'ignore').decode('ascii')
            data['label'] = row[-2]
            
            # get hashtags in this message 
            hashtags = get_hashtags(data['message'])
            data['hashtags'] = hashtags
            data['contains_hashtags'] = (1 if (len(hashtags)>1) else 0)
            data['amount_hashtags'] = len(hashtags)

            # get emojis in this message
            emojis = get_emojis(data['message'])
            data['emojis'] = emojis
            data['contains_emojis'] = (1 if (len(emojis)>1) else 0) 
            data['amount_emojis'] = len(emojis)

            # get retweets in this message
            retweets = get_retweets(data['message'])
            data['retweets'] = retweets
            data['contains_retweets'] = (1 if (len(retweets)>1) else 0)
            data['amount_retweets'] = len(retweets) 

            # get marked users
            marked_users = get_users(data['message'])
            data['marked_users'] = marked_users
            data['contains_marked_users'] = (1 if (len(marked_users)>1) else 0)
            data['amount_marked_users'] = len(marked_users)

            # get URLs 
            urls = get_urls(data['message'])
            data['urls'] = urls
            data['contains_urls'] = (1 if (len(urls)>1) else 0)
            data['amount_urls'] = len(urls)

            data['clean_message'] = clean_message(data['message'])
    
            # divide messages
            if (data['label'] == '0'):
                dataset[0].append(data)
            elif (data['label'] == '1'):
                dataset[1].append(data)
            elif (data['label'] == '2'):
                dataset[2].append(data)

            #print(data)
        print (len(dataset[0]), len(dataset[1]), len(dataset[2]))
        
        tmp = [[], []]
        tmp[0] = dataset[1] # offensive language
        tmp[1] = dataset[2] # neither
        new_dataset_train, new_dataset_test = separate_dataset(tmp, 0.6, 0.4)

        f = open("dataset/train/positive.txt","w+")
        for elem in new_dataset_train[0]:
            f.write(json.dumps(elem) + '\n') 
        f.close()

        f = open("dataset/train/negative.txt","w+")
        for elem in new_dataset_train[1]:
            f.write(json.dumps(elem) + '\n') 
        f.close()

        f = open("dataset/test/positive.txt","w+")
        for elem in new_dataset_test[0]:
            f.write(json.dumps(elem) + '\n') 
        f.close()

        f = open("dataset/test/negative.txt","w+")
        for elem in new_dataset_test[1]:
            f.write(json.dumps(elem) + '\n') 
        f.close()

read_csv_file()