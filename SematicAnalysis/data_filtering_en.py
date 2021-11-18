from nltk import *
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

#get the data
short_pos = open("./data/user_pos.txt", "r", encoding='UTF-8').read()
short_neg = open("./data/user_neg.txt", "r", encoding='UTF-8').read()

documents = []
#get the postive words
for r in short_pos.split('\n'):
    documents.append((r, "pos"))

for r in short_neg.split('\n'):
    documents.append((r, "neg"))

all_words = []

short_pos_words = word_tokenize(short_pos)
short_neg_words = word_tokenize(short_neg)

for w in short_pos_words:
    all_words.append(w.lower())

for w in short_neg_words:
    all_words.append(w.lower())

print(all_words)

# Tokenization
# print(sent_tokenize(short_pos))
# print(word_tokenize(short_pos))
# print(sent_tokenize(short_neg))
# print(word_tokenize(short_neg))

#stopwords
stop_words = set(stopwords.words('english'))
word_tokens = word_tokenize(short_neg)#change this line to save different type of file
filtered_sentence = [w for w in word_tokens if not w in stop_words]
filtered_sentence = []
for w in word_tokens:
    if w not in stop_words:
        filtered_sentence.append(w)

# print(word_tokens)
# print(filtered_sentence)


#stemming
ps = PorterStemmer()
stemming_sentence=[]
for w in filtered_sentence:
    stemming_sentence.append(w)
# print(stemming_sentence)
# print(ps.stem(w) for w in filtered_sentence)

# Lemmatization
wnl = WordNetLemmatizer()
wnl_sentence=[]
for w in stemming_sentence:
    wnl_sentence.append(w)
# print(wnl_sentence)
# print([wnl.lemmatize(t) for t in filtered_sentence])


# with open("./data/sent_pos.txt",'wt', encoding='UTF-8') as f:
#     for i in (sent_tokenize(short_pos)):
#         print(i, file=f)
#
# with open("./data/sent_neg.txt",'wt', encoding='UTF-8') as f:
#     for i in (sent_tokenize(short_neg)):
#         print(i, file=f)
#
# with open("./data/word_pos.txt",'wt', encoding='UTF-8') as f:
#     for i in (word_tokenize(short_pos)):
#         print(i, file=f)
#
# with open("./data/word_neg.txt",'wt', encoding='UTF-8') as f:
#     for i in (word_tokenize(short_neg)):
#         print(i, file=f)