# Sematic Analysis


## Getting Started

Start by exporting data from database with label. We should both export the pos and neg data.

```
select
    ut.user_comment
from
    user_table ut
where 
    ut.user_rate='Recommended';
```

Then we should install nltk with the following code, to download some neccessary libiraries.


```
import nltk
nltk.download()
```

## Structure of Files


```
E:.
│  classify_en.py
│  classify_en_module.py
│  classify_en_module_use.py
│  data_filtering_en.py
│  README.md
│  wordcloud_cn.py
│  wordcloud_en.py
│  __init__.py
│
├─data
│      background.png
│      sent_neg.txt
│      sent_pos.txt
│      stop.txt
│      user_combined.txt
│      user_neg.txt
│      user_pos.txt
│      user_pos_cn.txt
│      word_pos.txt
│
├─pickled_algos
│      BernoulliNB_classifier.pickle
│      documents.pickle
│      LinearSVC_classifier.pickle
│      LogisticRegression_classifier.pickle
│      MNB_classifier.pickle
│      originalnaivebayes.pickle
│      SGDC_classifier.pickle
│      word_features.pickle
│
└─result
        background.png
        word_pos_en.png
        pos_wordcloud_pos_cn.png
```

## The functions of files
classify_en: to use data train the data and then test the model and do the predictions.

classify_en_module and classify_en_module is to create frozen model and use the frozen model to do predictions.

data_filtering: is to do the Data preparation.

wordcloud is to create wordcloud for en and cn.

pickled_algos files are the frozen models to directly use without training.