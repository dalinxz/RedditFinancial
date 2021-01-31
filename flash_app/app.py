# -*- coding: utf-8 -*-

# app.py
from flask import Flask, session        # import flask
from flask import render_template, request
from forms import front_page_form, search_results_form
from flask import render_template, flash, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
import requests

import pandas as pd
import time
import nltk
import praw
import time
import requests 
import requests.auth
import pandas as pd
import spacy
from tqdm import tqdm
from rank_bm25 import BM25Okapi
nltk.download('punkt')

ID = ''
app = Flask(__name__)             # create an app instance
app.config['SECRET_KEY'] = 'you-will-never-guess'
@app.route("/", methods=['GET', 'POST'])              # at the end point /<name>
def index():
    form = front_page_form()
    get_data = get_top_3()
    data = [{'url': get_data[0]}, 
            {'url': get_data[1]},
            {'url': get_data[2]}
        ]
    if form.validate_on_submit():
        session['search_val'] = form.search_box.data
        return redirect('/search_results')
    return render_template('index.html', form=form, data=data)


@app.route("/search_results", methods=['GET', 'POST'])
def search_results():
    form = search_results_form()
    search_val = session.get('search_val', None)
    results = search(search_val)
    return render_template('search_results.html', form=form, data=results)

def construct_corpus(df): # gets all posts to one string
  corpus = ""
  for i in df['Message body']:
      corpus += i
      
  return corpus

def key_builder(corpus): # constructs keyword dictionary for each data frame
  stopwords = ["Autist", "fuck", "https", "THE", "n't", "'s", "'", "the", "I", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]
  tokens = nltk.word_tokenize(corpus)

  keys = {}
  for word in tokens:
    word = word.replace(".","")
    word = word.replace(" ", "")
    word = word.replace('”', "")
    word = word.replace('“', "")
    word = word.replace('[', "")
    word = word.replace(']', "")
    word = word.replace('(', "")
    word = word.replace(')', "")
    word = word.replace(",","")
    word = word.replace("%", "")
    word = word.replace("''", "")
    word = word.replace(";", "")
    word = word.replace("’", "")
    word = word.replace('?', "")
    word = word.replace("&", "")
    word = word.replace('/', "")
    word = word.replace(":","")
    word = word.replace("\"","")
    word = word.replace("!","")
    word = word.replace("â€œ","")
    word = word.replace("â€˜","")
    word = word.replace("*","")
    word = word.replace("``", "")
    word = word.replace("'m", "")
    word = word.replace("-", "")
    if word not in stopwords:
        if word not in keys:
            keys[word] = 1
        else:
            keys[word] += 1

  temp = pd.DataFrame(list(keys.items()), columns = ['Word','Count'])
  temp.sort_values(by=['Count'], inplace=True, ascending=False)

  return temp[0:50]

def keyword_parser(df, keys_dict): # parses the body of each posts, records how many keywords appear 
  keyword_scores = []
  for body in df['Message body']:
    x = 0
    for word in body:
      if word in keys_dict.Word.tolist():
        x += 1
    keyword_scores.append(x)
    
  return keyword_scores

def scorer(df): #. Y = a1x1 + a2x2... where x1, x2 and so on are variables that mark a 'good post'
  Y = []
  for index, row in df.iterrows():
    a1 = .25
    a2 = .25 
    a3 = 4
    calculated = a1*row['Score of Post'] + a2*row['#Comments'] + a3*row.keyword_scores
    Y.append(calculated)
  df['Y'] = Y

def pick_posts(dfwsb, dfoptions, dffinind, radio, time_check = time.time() - 259200):
  max_post_url_1 = ""
  max_post_url_2 = ""
  max_post_url_3 = ""

  if radio[0] == 1 and radio[1] == 1 and radio[2] == 1:
    # one post from each subreddit
    df_recent_wsb = dfwsb[dfwsb.TimeStamp > time_check]
    df_recent_wsb.sort_values(by=['Y'], inplace=True, ascending=False)

    df_recent_options = dfoptions[dfoptions.TimeStamp > time_check]
    df_recent_options.sort_values(by=['Y'], inplace=True, ascending=False)

    df_recent_finind = dffinind[dffinind.TimeStamp > time_check]
    df_recent_finind.sort_values(by=['Y'], inplace=True, ascending=False)
    
    max_post_url_1 = df_recent_wsb['URL'].iloc[0]
    max_post_url_2 = df_recent_options['URL'].iloc[1]
    max_post_url_3 = df_recent_finind['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]
    
  elif radio[0] == 1 and radio[1] == 1 and radio[2] == 0:
    # two posts from one, one from another
    df_recent_wsb = dfwsb[dfwsb.TimeStamp > time_check]
    df_recent_wsb.sort_values(by=['Y'], inplace=True, ascending=False)

    df_recent_options = dfoptions[dfoptions.TimeStamp > time_check]
    df_recent_options.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_wsb['URL'].iloc[0]
    max_post_url_2 = df_recent_wsb['URL'].iloc[1]
    max_post_url_3 = df_recent_options['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]

  elif radio[0] == 0 and radio[1] == 1 and radio[2] == 1:
    # two posts from one, one from another
    df_recent_options = dfoptions[dfoptions.TimeStamp > time_check]
    df_recent_options.sort_values(by=['Y'], inplace=True, ascending=False)

    df_recent_finind = dffinind[dffinind.TimeStamp > time_check]
    df_recent_finind.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_options['URL'].iloc[0]
    max_post_url_2 = df_recent_options['URL'].iloc[1]
    max_post_url_3 = df_recent_finind['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]

  elif radio[0] == 1 and radio[1] == 0 and radio[2] == 1:
    # two posts from one, one from another
    df_recent_wsb = dfwsb[dfwsb.TimeStamp > time_check]
    df_recent_wsb.sort_values(by=['Y'], inplace=True, ascending=False)
    
    df_recent_finind = dffinind[dffinind.TimeStamp > time_check]
    df_recent_finind.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_wsb['URL'].iloc[0]
    max_post_url_2 = df_recent_finind['URL'].iloc[1]
    max_post_url_3 = df_recent_finind['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]

  elif radio[0] == 1 and radio[1] == 0 and radio[2] == 0:
    # three posts from one
    df_recent_wsb = dfwsb[dfwsb.TimeStamp > time_check]
    df_recent_wsb.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_wsb['URL'].iloc[0]
    max_post_url_2 = df_recent_wsb['URL'].iloc[1]
    max_post_url_3 = df_recent_wsb['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]

  elif radio[0] == 0 and radio[1] == 0 and radio[2] == 1:
    # three posts from one
    df_recent_finind = dffinind[dffinind.TimeStamp > time_check]
    df_recent_finind.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_finind['URL'].iloc[0]
    max_post_url_2 = df_recent_finind['URL'].iloc[1]
    max_post_url_3 = df_recent_finind['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]
    
  elif radio[0] == 0 and radio[1] == 1 and radio[2] == 0:
    # three posts from one
    df_recent_options = dfoptions[dfoptions.TimeStamp > time_check]
    df_recent_options.sort_values(by=['Y'], inplace=True, ascending=False)

    max_post_url_1 = df_recent_options['URL'].iloc[0]
    max_post_url_2 = df_recent_options['URL'].iloc[1]
    max_post_url_3 = df_recent_options['URL'].iloc[2]

    return [max_post_url_1, max_post_url_2, max_post_url_3]
    
  else: 
    pass

def get_top_3():
    wsb_df = pd.read_csv('https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/wallstreetbets(1).csv')
    options_df = pd.read_csv('https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/options(1).csv')
    finind_df = pd.read_csv('https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/financialindependence(2).csv')

    wsb_df.drop(columns='Flair', inplace=True)
    options_df.drop(columns='Flair', inplace=True)
    finind_df.drop(columns='Flair', inplace=True)

    wsb_df.dropna(inplace=True)
    options_df.dropna(inplace=True)
    finind_df.dropna(inplace=True)

    wsb_df.set_index('ID')
    options_df.set_index('ID')
    finind_df.set_index('ID')

    wsb_body = construct_corpus(wsb_df)
    options_body = construct_corpus(options_df)
    finind_body = construct_corpus(finind_df)

    keys_dict_wsb = key_builder(wsb_body)
    keys_dict_options = key_builder(options_body)
    keys_dict_finind = key_builder(finind_body)

    wsb_df['keyword_scores'] = keyword_parser(wsb_df, keys_dict_wsb)
    options_df['keyword_scores'] = keyword_parser(options_df, keys_dict_options)
    finind_df['keyword_scores'] = keyword_parser(finind_df, keys_dict_finind)

    scorer(wsb_df)
    scorer(options_df)
    scorer(finind_df)

    filter = [1,1,1]

    return pick_posts(wsb_df, options_df, finind_df, filter)

    # wsb_df.head()
    # options_df.head()
    # finind_df.head()

def search(input_text):
    url = 'https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/options(1).csv'
    options_df = pd.read_csv(url, index_col=0)
    url = 'https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/financialindependence(2).csv'
    finInd_df = pd.read_csv(url, index_col=0)
    url = 'https://raw.githubusercontent.com/enanpurrp/Debullshitiser/main/wallstreetbets(1).csv'

    WSB_df = pd.read_csv(url, index_col=0)
    huge_df = options_df.append(finInd_df,ignore_index=True)
    huge_df = huge_df.append(WSB_df,ignore_index=True)
    return search_engine(huge_df, input)

def search_engine(huge_df, input_text):
    nlp = spacy.load("en_core_web_sm")
    tok_text=[] # for our tokenised corpus
    #Tokenising using SpaCy:
    text_list = huge_df.Title.str.lower().values
    for doc in tqdm(nlp.pipe(text_list, disable=["tagger", "parser","ner"])):
        tok = [t.text for t in doc if t.is_alpha]
        tok_text.append(tok)

    bm25 = BM25Okapi(tok_text)

    tokenized_input = input.lower().split(" ")
    import time

    t0 = time.time()
    results = bm25.get_top_n(tokenized_input, huge_df.Title.values, n=3)
    t1 = time.time()
    #print(f'Searched by title across subreddits in {round(t1-t0,3) } seconds \n')
    '''for i in results:
        print(i)'''
    return results


if __name__ == "__main__":
    port_used = 5001
    app.run(port=port_used) 
                          # run the flask app
    
    