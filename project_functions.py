#%%
import pandas as pd


#%% 
# Variables
upwindow = 7
lowwindow = 2

'''
Preprocessing fuction for both the children as the parents
'''
def preprocessing_child(children):    
    # Children
    children.loc[:,'title'] = children.loc[:,'title'].str.lower()
    children.loc[:,'content'] = children.loc[:,'content'].str.lower()
    children['related_parents'] = children['related_parents'].str.replace('matches/','').str.split(',')
    children.loc[:,'publish_date_date'] = pd.to_datetime(children.loc[:,'publish_date_date'])
#    children.loc[:,'content'] = children.loc[:,'content'].str.replace('-',' ') Breaks check_link
#    children.loc[:,'content'] = children.loc[:,'content'].str.replace('  ',' ')
    
    # replace other references to cbs with cbs itself
    children.loc[:,'content'] = children.loc[:,'content'].str.replace('centraal bureau voor de statistiek','cbs')
    children.loc[:,'content'] = children.loc[:,'content'].str.replace('cbs(cbs)','cbs')
    children.loc[:,'content'] = children.loc[:,'content'].str.replace('cbs (cbs)','cbs')
    children.loc[:,'content'] = children.loc[:,'content'].str.replace('cbs ( cbs )','cbs')
    return children



def remove_stopwords_from_content(row, column = 'content'):
    '''
    Function to remove stopwords from the content and return it as a string.
    '''
    import nltk
    from nltk.corpus import stopwords
    import re
    stop_words = set(stopwords.words('dutch'))
    
    filtered_content = ''                                                 # Set as empty string for rows without content
    content = row[column]
    if type(content) != float:                                          # Some parents have no content (nan)
        content = re.sub(r'[^\w\s]','',content)                             # Remove punctuation
        content = nltk.tokenize.word_tokenize(content)
        filtered_content = [w for w in content if not w in stop_words]      # Remove stopwords
    return ' '.join(filtered_content)                                     # Convert from list to space-seperated string

