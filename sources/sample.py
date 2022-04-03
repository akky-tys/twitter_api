import datetime, time
import urllib3
import urllib
import setting
import json
import twitterApi
import pandas as pd
import numpy as np
import csv 
import MeCab  as mb
from gensim.models import word2vec


def getTweet(fileName, keyword):
  http = urllib3.PoolManager()
  KEY  = setting.TWITTER_BEARER_TOKEN
  
  params = {
            'query'        : keyword,
            'max_results'  : 100,
            'expansions'   : 'author_id,attachments.media_keys', 
            'tweet.fields' : 'created_at,lang,entities',
            'user.fields'  : 'name'
            }

  with open( fileName + ".csv",'a') as f:
    writer = csv.writer(f)
    tweets = twitterApi.getTweetByText(http, KEY, params)
    time.sleep(5)
    hasNextToken = True
    while hasNextToken:
      for tweet in tweets['data']:
        l_tags, l_annotations = [], []
        if ('entities' in tweet) :

          if ('hashtags' in tweet['entities']) :
            l_tags = [d.get('tag') for d in tweet['entities']['hashtags']];

          if ('annotations' in tweet['entities']) :
            l_annotations = [d.get('normalized_text') for d in tweet['entities']['annotations']];
        
        
        writer.writerow([tweet['id'],tweet['author_id'], tweet['created_at'], tweet['text'],l_tags,l_annotations])
        
      if ('meta' in tweets):
        if ('next_token' in tweets['meta']) :
          params['next_token'] = tweets['meta']['next_token']
          time.sleep(5)
          tweets = twitterApi.getTweetByText(http, KEY, params)
        else :
          hasNextToken = False



def getStopwords():
  url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
  res = urllib.request.urlopen(url)

  slothlib_stopwords  = [row.decode("utf-8").strip() for row in res]
  slothlib_stopwords  = [ss for ss in slothlib_stopwords if not ss==u'']
  return slothlib_stopwords

def parseByMecab(text):
  tagger = mb.Tagger('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd -u /home/20200920_python/python-twitter/personList.dic')
  word_list = []
  node = tagger.parseToNode(text)
  while node:
    pos = node.feature.split(",")[0]
    if pos in ["名詞", "動詞", "形容詞"]:
      word = node.surface; ##区切られたワードを取ってくる
      word_list.append(word)
    node = node.next
  return "\n".join(word_list).strip()


def delStopwords(text,stopwords):
  word = [word for word in text.split(" ") if not word in stopwords]
  words = "\n".join(word).strip()
  return words

def makeWord2VecModel(fileName):
  ## pandasでCSV取り込み　dataFream型で返却されるので便利
  stopwords = getStopwords();
  tweet_df = pd.read_csv(fileName + '.csv', names=('id', 'author_id', 'created_at', 'text', 'tags', 'annotations'))
  tweet_df['mecabText'] = tweet_df['text'].apply(lambda x: parseByMecab(x))
  tweet_df['delStopWordText']  = tweet_df['mecabText'].apply(lambda x:delStopwords(x, stopwords))
  sent  = [token.split("\n") for token in tweet_df['delStopWordText']] 
  ## sent    = list(tweet_df['mecabText'])
  model = word2vec.Word2Vec(sent, size = 100, min_count = 3, window = 5)
  model.save(fileName+'size100-min3-win5.model' )



def makeDataFile3(fileName):
  tweet_df = pd.read_csv(fileName + '.csv', names=('id', 'author_id', 'created_at', 'text', 'tags', 'annotations'))
  results = []
  for tok in tweet_df['text']:
    results.append(makeMecab(tok))
  with open("test_list.txt", "a", encoding="utf-8") as fp:
    fp.write("\n".join(results))

  data = word2vec.LineSentence('test_list.txt')
  model = word2vec.Word2Vec(data, size=100, window=1, hs=1, min_count=1, sg=1)
  model.save("test_model.model")


def checkWordSimilar(fileName,word):

  model = word2vec.Word2Vec.load(fileName)
  
  try :
    results  = model.wv.most_similar(positive=word, topn = 30)
    for i,result in enumerate(results):
        print ( i+1 ,' [', result[0] ,'] : スコア=' , result[1])
    df_result = pd.DataFrame(results, columns=["word", "sim"])
    print(df_result.T)
  except KeyError as error:
    print(error);


def checkWordCalc(fileName, posiWords, negaWords):

  model = word2vec.Word2Vec.load(fileName)
  
  try :
    results  = model.wv.most_similar(positive=posiWords, negative=negaWords)
    for i,result in enumerate(results):
        print ( i+1 ,' [', result[0] ,'] : スコア=' , result[1])
  except KeyError as error:
    print(error);


