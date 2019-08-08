Small test of the feasibility of predicting the themes of newsarticles that refer to CBS research

First did some basic preprocessing of the children and modified the df to have one theme per record. Some articles have multiple themes.

Selected themes that occured more often than 100
Removed stopwords based on nltk dutch list

Trained NaiveBayes model on the TF-IDF of the content of the children

Removed stopwords based on nltk dutch list
Accuracy: 0.6023

Trained NaiveBayes model on the BM25 of the content of only 5000 children (more took too long)
Accuracy:0.425 (expected to be higher than TF-IDF for whole dataset

If Tf-IDF of same 5000 children:
Accuracy: 0.406
