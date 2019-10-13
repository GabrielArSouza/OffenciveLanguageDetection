import csv, sys, re, json

FILENAME = "dataset/labeled_data.csv"

def clean_message (message):
    tmp = re.sub(r'RT @[a-zA-Z0-9_]*','', message) # remove retweets
    tmp = re.sub(r'@[a-zA-Z0-9_]*','', tmp)        # remove users
    tmp = re.sub(r'#[0-9a-zA-Z]+','', tmp)         # remove hashtags
    tmp = re.sub(r'&#[0-9]*;', '', tmp)            # remove emojis
    tmp = re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})', '', tmp)
    tmp = re.sub(r'[^\w\s]','', tmp)               # remove punctuation
    return tmp

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

def read_csv_file ():
    
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
    
            print(data)


read_csv_file()