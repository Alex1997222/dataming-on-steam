import re
import collections
import numpy as np
import jieba
import wordcloud
from PIL import Image
import matplotlib.pyplot as plt

# get the data
fn = open('data/user_pos_cn.txt', 'r', encoding='utf-8') # open the file
string_data = fn.read()
fn.close()

# use re to remove some tokens
pattern = re.compile(u'\t|\n|\.|-|:|;|\)|\(|\?|"')
string_data = re.sub(pattern, '', string_data)

# use jieba to cut some Chinese words
seg_list_exact = jieba.cut(string_data, cut_all = False) # use the precise mode
object_list = []
remove_words = [u'的', u'，',u'和', u'是', u'随着', u'对于', u'对',u'等',u'能',u'都',u'。',u' ',u'、',u'中',u'在',u'了',
                u'通常',u'如果',u'我们',u'需要'] # Some Chinese Stopwords.

for word in seg_list_exact:
    if word not in remove_words:
        object_list.append(word)

word_counts = collections.Counter(object_list) # count the frequency.
word_counts_top10 = word_counts.most_common(10) # show the most common words
print (word_counts_top10) # check the output
word_counts_top10 = str(word_counts_top10)

# show the result
mask = np.array(Image.open('data/background.png'))
wc = wordcloud.WordCloud(
    font_path='simfang.ttf', # basic set
    mask=mask, # set the background
    max_words=200,
    max_font_size=150,
    background_color='white',
    width=800, height=600,
)

wc.generate_from_frequencies(word_counts) # create the wordcloud
plt.imshow(wc) # show the wordcloud
plt.axis('off')
plt.show() # show the picture
wc.to_file('./result/pos_wordcloud_cn.png')