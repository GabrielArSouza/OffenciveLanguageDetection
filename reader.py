import csv
import sys 
import re

def tokenizer_retweets (twitter):
	
	# remove emojis
	twitter.encode('ascii', 'ignore').decode('ascii')	
	words = twitter.split(' ')

	regex = re.compile('@+')	
	retweets = []

	for word in words:
		if regex.match(word) and len(word.strip()) > 1:
			word = re.sub(r':', '', word)
			retweets.append(word)
	
	return retweets
				
def tokenizer_hastags (twitter):
	twitter.encode('ascii', 'ignore').decode('ascii')	
	words = twitter.split(' ')

	regex = re.compile('#+')

	hastags = []

	for word in words:
		if regex.match(word) and len(word.strip()) > 1:
		 	hastags.append(word)

	return hastags


def reader_csv_file (filename):
	data = {}
	with open(filename) as csvfile:
		read_csv = csv.reader(csvfile, delimiter=',')
		count = 0;
		for row in read_csv:
			tmp = {}

			twitter = row[len(row)-1]	
			tmp['original_message'] = twitter

			# classes 
			# 0 - hate speech
			# 1 - Offensive language
			# 2 - neither
			tmp['class'] = row[len(row)-2]


			# remove punctuation
			# punctuation marks 
			punctuations = '''!()-[]{};:'"\,<>./?$%^*_~'''

			# traverse the given string and if any punctuation 
			# marks occur replace it with null 
			for x in twitter.lower(): 
				if x in punctuations: 
					twitter = twitter.replace(x, "") 	

			retweets = tokenizer_retweets(twitter)
			if len(retweets) >= 1:
				tmp['retweets'] = 'yes'
				tmp['retweets_value'] = retweets
			else:
				tmp['retweets'] = 'no'
				tmp['retweets_value'] = []	
			
			hastags = tokenizer_hastags(twitter)
			if len(hastags) >= 1:
				tmp['hastags'] = 'yes'
				tmp['hastags_value'] = hastags
			else:
				tmp['hastags'] = 'no'
				tmp['hastags_value'] = []	

			print (tmp)
			print ('>>>>>>>>>>>>>>>>>>')			
			
			data[count] = tmp
			count = count + 1			
	
	#print (data)

filename = sys.argv[1]
reader_csv_file (filename)








