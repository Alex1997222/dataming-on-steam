import os
from os import path
from wordcloud import WordCloud
from matplotlib import pyplot as plt
d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
# get the text
text = open(path.join(d,'./data/word_neg.txt'),encoding='UTF-8').read()
# create the wordCLoud
wc = WordCloud(scale=2,max_font_size = 100)
wc.generate_from_text(text)
# Show the wordCloud
plt.imshow(wc,interpolation='bilinear')
plt.axis('off')
plt.tight_layout()
#save the png
wc.to_file('./result/word_neg_en.png')
plt.show()