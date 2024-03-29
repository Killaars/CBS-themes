#%% 
import pandas as pd
from pathlib import Path
import datetime
import pickle

from project_functions import preprocessing_child,remove_stopwords_from_content
#%%
path = Path('/Users/rwsla/Lars/CBS_2_mediakoppeling/data/solr/')
#path = Path('/flashblade/lars_data/CBS/CBS2_mediakoppeling/data/solr/')

children = pd.read_csv(str(path / 'related_children.csv'),index_col=0)

# do the preprocessing of the children. Defined in script functions.
children = preprocessing_child(children)

# Melt the themes and create one theme per record
children_themes = children[['id','themes']]
children_themes.loc[:,'themes'] = children_themes['themes'].str.split(',')
children_themes = children_themes['themes'].apply(pd.Series) \
    .merge(children_themes, right_index = True, left_index = True) \
    .drop(["themes"], axis = 1)\
    .melt(id_vars = ['id'], value_name = "theme")\
    .drop("variable", axis = 1) \
    .dropna()
    
children_themes['theme'].value_counts()

# Merge content into df

children_themes = children_themes.merge(children[['content','id']],how='left',on='id')

# Select only the themes that occur often

theme_counts = children_themes['theme'].value_counts()
theme_lists = theme_counts[theme_counts > 100].index.tolist()
children_capped_themes = children_themes[children_themes['theme'].isin(theme_lists)]
children_capped_themes = children_capped_themes[children_capped_themes['theme']!='Vrije nieuwsgaring']
children_capped_themes['theme'].value_counts()
#%% Remove stopwords
children_capped_themes.loc[:,'content'] = children_capped_themes.apply(remove_stopwords_from_content,args=('content',),axis=1)

#%% Label encoding
from sklearn.preprocessing import LabelEncoder
labelencoder = LabelEncoder()
children_capped_themes.loc[:,'encoded_label'] = labelencoder.fit_transform(children_capped_themes.loc[:, 'theme'])
#%% make tfidf from content
from sklearn.feature_extraction.text import TfidfVectorizer
a = datetime.datetime.now()
tf=TfidfVectorizer()
text_tf= tf.fit_transform(children_capped_themes['content'])

# Split in train and test
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    text_tf, children_capped_themes['encoded_label'], test_size=0.2, random_state=123)
#%%
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)

#print('Saving model...')
#filename = 'MultiNB_tf.sav'
#pickle.dump(clf, open(filename, 'wb'))

predicted= clf.predict(X_test)
print("MultinomialNB Accuracy TF-IDF:",metrics.accuracy_score(y_test, predicted))
b = datetime.datetime.now()
c=b-a
print(c)

#%% Do the same but with BM25 weights. Takes long time for all children! but is probably more accurate
from gensim.summarization.bm25 import get_bm25_weights
children_capped_themes.loc[:,'splitted_content'] = children_capped_themes.loc[:,'content'].str.split(' ')
#%%
a = datetime.datetime.now()
print('busy with BM25')
small_test = children_capped_themes.sample(n=5000)
BM25 = get_bm25_weights(small_test.loc[:,'splitted_content'])
#%%
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    BM25, small_test['encoded_label'], test_size=0.2, random_state=123)
#%%
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
# Model Generation Using Multinomial Naive Bayes
clf = MultinomialNB().fit(X_train, y_train)

filename = 'MultiNB_BM25.sav'
pickle.dump(clf, open(filename, 'wb'))

predicted= clf.predict(X_test)
print("MultinomialNB Accuracy BM25:",metrics.accuracy_score(y_test, predicted))
b = datetime.datetime.now()
c=b-a
print(c)

