# -*- coding: utf-8 -*-
"""Experimentos2.0.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FH21162gpRNP8JWhyAVx-GZrd_kBrrLI

#Imports
"""

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from gensim.models.doc2vec import Doc2Vec, TaggedDocument
from gensim.models.word2vec import Word2Vec
import gensim
import nltk
import re
import string
from collections import defaultdict
from sklearn.model_selection import train_test_split
import multiprocessing
from datetime import datetime
import sys

#Models (Classification and metrics)
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score, make_scorer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV

"""#Load dataset"""

df_fakes = pd.read_csv('datasetBoatosTratado.csv')
df_true = pd.read_csv('clean-g1.csv')
df_fakes_lupa = pd.read_csv('data-lupa-agosto.csv')

df_fakes = df_fakes.dropna()
df_fakes['classification'] = 1
del df_fakes_lupa["Unnamed: 0"]
df_fakes_lupa['classification'] = df_fakes_lupa['classification'].apply(lambda x: str.strip(x))
print('Fakes Boatos shape', df_fakes.shape)
print('True News Boatos shape', df_true.shape)
print('Fakes Lupa shape', df_fakes_lupa.shape)

df_fakes_lupa = df_fakes_lupa.loc[df_fakes_lupa['classification'].str.match('Falso')]

df_fakes_lupa['classification'] = df_fakes_lupa['classification'].replace({'Falso': 1})

# df_fakes_all = pd.concat([df_fakes[['text', 'classification']], df_fakes_lupa[['text', 'classification']]])
# df_fakes_all.shape

"""#Text Analysis

##Functions
"""

def count_characters(doc):
  count = 0
  for char in doc:
    if char == ' ': continue
    count += 1
  return count

def count_characters_per_word(doc):
  count = []
  for word in doc.split():
    count.append(count_characters(word)) 
  
  return np.mean(count)

def count_words_per_sentence_avg(doc):
  words = []
  for sentence in re.split('\.|!|\?', doc):
    if sentence == '' or sentence == ' ' : 
      continue
    words.append(len(sentence.split()))
  return np.mean(words)

def count_punctuation_per_sentence_avg(doc):
  punctuations = []
  #https://stackoverflow.com/questions/6969268/counting-letters-numbers-and-punctuation-in-a-string/14229674
  count = lambda l1,l2: sum([1 for x in l1 if x in l2]) 
  for sentence in re.split('\.|!|\?', doc):
    if sentence == '' or sentence == ' ' : 
      continue
    punctuations.append(count(sentence, string.punctuation))
  return np.mean(punctuations)

"""##Boatos"""

#Words per document
df_fakes['words_count'] = df_fakes['text'].apply(lambda x: len(x.split()))
#Characters per document
df_fakes['caracters_count'] = df_fakes['text'].apply(lambda x: count_characters(x))
#Sentences per document
df_fakes['sentences_count'] = df_fakes['text'].apply(lambda x: len(x.split('.')))

#AVG characters per word
df_fakes['characters_per_word_avg'] = df_fakes['text'].apply(lambda x: count_characters_per_word(x))
#AVG words per sentence
df_fakes['words_per_sentence_avg'] = df_fakes['text'].apply(lambda x: count_words_per_sentence_avg(x))
#AVG punctuations per sentence
df_fakes['punctuations_per_sentence'] = df_fakes['text'].apply(lambda x: count_punctuation_per_sentence_avg(x))

df_fakes['date'] = pd.to_datetime(df_fakes['date'])
df_fakes.index = df_fakes['date']
del df_fakes['date']
df_fakes.sort_index(inplace=True)

max(df_fakes.index)

min(df_fakes.index)

df_fakes.describe()

"""##Lupa"""

#Words per document
df_fakes_lupa['words_count'] = df_fakes_lupa['text'].apply(lambda x: len(x.split()))
#Characters per document
df_fakes_lupa['caracters_count'] = df_fakes_lupa['text'].apply(lambda x: count_characters(x))
#Sentences per document
df_fakes_lupa['sentences_count'] = df_fakes_lupa['text'].apply(lambda x: len(x.split('.')))

#AVG characters per word
df_fakes_lupa['characters_per_word_avg'] = df_fakes_lupa['text'].apply(lambda x: count_characters_per_word(x))
#AVG words per sentence
df_fakes_lupa['words_per_sentence_avg'] = df_fakes_lupa['text'].apply(lambda x: count_words_per_sentence_avg(x))
#AVG punctuations per sentence
df_fakes_lupa['punctuations_per_sentence'] = df_fakes_lupa['text'].apply(lambda x: count_punctuation_per_sentence_avg(x))

df_fakes_lupa['date'] = pd.to_datetime(df_fakes_lupa['date'])
df_fakes_lupa.index = df_fakes_lupa['date']
del df_fakes_lupa['date']
df_fakes_lupa.sort_index(inplace=True)

df_fakes_lupa = df_fakes_lupa[df_fakes_lupa['caracters_count']!=df_fakes_lupa['caracters_count'].min()]

df_fakes_lupa.describe()

df_fakes_lupa = df_fakes_lupa[df_fakes_lupa['caracters_count']!=df_fakes_lupa['caracters_count'].min()]

df_fakes_all = pd.concat([df_fakes[['text', 'classification','words_count',
                                    'caracters_count','sentences_count','characters_per_word_avg',
                                    'words_per_sentence_avg','punctuations_per_sentence']], 
                          df_fakes_lupa[['text', 'classification','words_count',
                                    'caracters_count','sentences_count','characters_per_word_avg',
                                    'words_per_sentence_avg','punctuations_per_sentence']]])

max(df_fakes_lupa.index)

min(df_fakes_lupa.index)


#Words per document
df_true['words_count'] = df_true['text'].apply(lambda x: len(x.split()))
#Characters per document
df_true['caracters_count'] = df_true['text'].apply(lambda x: count_characters(x))
#Sentences per document
df_true['sentences_count'] = df_true['text'].apply(lambda x: len(x.split('.')))

#AVG characters per word
df_true['characters_per_word_avg'] = df_true['text'].apply(lambda x: count_characters_per_word(x))
#AVG words per sentence
df_true['words_per_sentence_avg'] = df_true['text'].apply(lambda x: count_words_per_sentence_avg(x))
#AVG punctuations per sentence
df_true['punctuations_per_sentence'] = df_true['text'].apply(lambda x: count_punctuation_per_sentence_avg(x))

df_true.describe()

df_fakes_all.describe()

"""#Preprocessing

"""

nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords

def preprocessing(doc, language):
  document = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', ' ', doc, flags=re.MULTILINE)# Removing urls
  document = re.sub(r'[^A-Za-zzáàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ]+', ' ', document) #Remove special caracteres and numbers
  document = re.sub(r"\s+[a-zA-Z]\s+", ' ', document) # Single character removal
  document = document.strip() #Remove leading and trailing whitespaces
  #document = document.lower() #Put the text in lowercase

  tokens = nltk.word_tokenize(document)
  stem = nltk.stem.SnowballStemmer(language)

  for idx,word in enumerate(tokens):
    if word in stopwords.words(language): #Remove stop words
      tokens.remove(word)
    else:
      tokens[idx] = stem.stem(word) #Steamming word

  return ' '.join(tokens)

# corpus_df['processed_text'] = corpus_df['text'].map(preprocessing)
# corpus_df.head()

#Applying preprocessing in all dataset texts
df_fakes_all['processed_text'] = df_fakes_all['text'].apply(preprocessing, args=('portuguese',)) 
df_true['processed_text'] = df_true['text'].apply(preprocessing, args=('portuguese',))

df_all_boatos_lupa = pd.concat([df_fakes_all[['text','processed_text','classification','words_count',
                                    'caracters_count','sentences_count','characters_per_word_avg',
                                    'words_per_sentence_avg','punctuations_per_sentence']], 
                    df_true[['text','processed_text','classification','words_count',
                                    'caracters_count','sentences_count','characters_per_word_avg',
                                    'words_per_sentence_avg','punctuations_per_sentence']].iloc[:2808,:],
                    ])


datasets_dict = {
    'Boatos_Lupa': df_all_boatos_lupa,
}

"""#Utils

##Vectorization
"""

def vectorization(dataset, threshold):
  #Frequency Vectors
  fv_vectorizer = CountVectorizer(min_df=threshold)
  X_fv = fv_vectorizer.fit_transform(dataset).toarray()

  #Term Frequency Inverse Document Frequency
  tfid_vectorizer = TfidfVectorizer(use_idf=True, min_df=threshold)
  X_tfid = tfid_vectorizer.fit_transform(dataset).toarray()

  #Word2Vec
  token_list = []
  
  for doc in dataset:
    token_list.append(doc.split())
  
  cores = multiprocessing.cpu_count()

  w2v_model = Word2Vec(min_count=threshold,
                      window=2,
                      vector_size=300,
                      sample=6e-5, 
                      alpha=0.03, 
                      min_alpha=0.0007, 
                      negative=20,
                      workers=cores-1,
                      sg = 1)
  w2v_model.build_vocab(token_list, progress_per=100)

  w2v_model.train(token_list, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)

  X_w2v = create_mean_matrix_w2c(dataset, w2v_model)

  return [X_fv, X_tfid, X_w2v]

#Code based on http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
def create_mean_matrix_w2c(sentences, model):
  matrix = []
  for sentence in sentences:
    matrix.append([np.mean(model.wv[word]) if word in sentence.split() 
                  else 0.0 
                  for word in model.wv.index_to_key
                   ])
  return matrix

"""##Experiment"""

def run_experiments(hyperparameters = None,*,dataset, feature_config, gs_flag, classifier, 
                    preprocessing, vec_threshold, ):
  
  start = datetime.now()
  print('Start:', start)

  dataset_type = ''
  grid_search = ''
  with_preprocessing = ''

  if gs_flag == True:
    grid_search = 'Yes'
  else:
    grid_search = 'No'

  if preprocessing == True:
    with_preprocessing = 'Yes'
  else:
    with_preprocessing = 'No'

  experiment_log = 'Initiating experiment with:'+'\n Preprocessing: {} \n Grid Search: {} \n Classifier: {} \n Feature Config: {} \n'
  print(experiment_log.format(with_preprocessing, grid_search, classifier.__class__.__name__, feature_config))
  print('Initiating Vectorization...')  

  vecs = ''
  if preprocessing == True:
    vecs = vectorization(dataset['processed_text'], vec_threshold)
  else:
    vecs = vectorization(dataset['text'], vec_threshold)

  print('End Vectorization!!!')

  fv = vecs[0]
  tf_idf = vecs[1]
  w2v = np.asarray(vecs[2])

  if (feature_config == "FV"):
    data = fv
  elif (feature_config == "TF_IDF"):
    data = tf_idf
  elif (feature_config == "W2V"):
    data = w2v
  elif (feature_config == "Features_Textuais"):
    data = dataset[['words_count',
                              'caracters_count',
                              'sentences_count',
                              'characters_per_word_avg',
                              'words_per_sentence_avg',
                              'punctuations_per_sentence']]
  elif (feature_config == "TF_IDF_Features_Textuais"):
    data = np.c_[tf_idf, dataset[['words_count',
                              'caracters_count',
                              'sentences_count',
                              'characters_per_word_avg',
                              'words_per_sentence_avg',
                              'punctuations_per_sentence']]]
  elif (feature_config == "FV_Features_Textuais"):
    data = np.c_[fv, dataset[['words_count',
                              'caracters_count',
                              'sentences_count',
                              'characters_per_word_avg',
                              'words_per_sentence_avg',
                              'punctuations_per_sentence']]]
  elif (feature_config == "W2V_Features_Textuais"):
    data = np.c_[w2v, dataset[['words_count',
                              'caracters_count',
                              'sentences_count',
                              'characters_per_word_avg',
                              'words_per_sentence_avg',
                              'punctuations_per_sentence']]]
  elif (feature_config == "ALL"):
    data = np.concatenate((fv,tf_idf,w2v), axis=1)
    data = np.c_[data, dataset[['words_count',
                                'caracters_count',
                                'sentences_count',
                                'characters_per_word_avg',
                                'words_per_sentence_avg',
                                'punctuations_per_sentence']]]

  
  Y = dataset['classification']
                                  
  X_train, X_test, y_train, y_test = train_test_split(data,Y, 
                                                      test_size=0.2, 
                                                      shuffle=True)
  print("X treino:", X_train.shape)
  print("X teste:", X_test.shape)
  print("Y treino:", y_train.shape)
  print("Y teste:", y_test.shape)

  if gs_flag == True:
    grid_search = GridSearchCV(estimator = classifier, 
                                param_grid = hyperparameters, 
                                cv = 5, verbose = 0)
    
    print("Initiating Grid Search...")    
    grid_search.fit(X_train, y_train)
    print("End Grid Search!!!")
    print('Grid Search selected parameters: {}'.format(grid_search.best_params_))
    predict_classifier = grid_search
  else:
    classifier.fit(X_train, y_train)
    predict_classifier = classifier

  array_accuracy = []
  array_precision = []
  array_recall = []
  array_f1 = []
  array_specificity = []

  for x in range(1,31):
    predictions = predict_classifier.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    array_accuracy.append(accuracy)

    precision = precision_score(y_test, predictions)
    array_precision.append(precision)

    recall = recall_score(y_test, predictions)
    array_recall.append(recall)

    f1 = f1_score(y_test, predictions)
    array_f1.append(f1)

    cm = confusion_matrix(y_test, predictions)
    specificity = cm[1,1]/(cm[1,0]+cm[1,1])
    array_specificity.append(specificity)

  print("Results:")
  print('Accuracy: \n Mean: {:.2f}% STD: {}'.format(np.mean(array_accuracy)*100, 
                                                  np.std(array_accuracy))) 
  print('Precision: \n Mean: {:.2f}% STD: {}'.format(np.mean(array_precision)*100, 
                                                  np.std(array_precision)))
  print('Recall: \n Mean: {:.2f}% STD: {}'.format(np.mean(array_recall)*100, 
                                                np.std(array_recall)))
  print('F1 score: \n Mean: {:.2f}% STD: {}'.format(np.mean(array_f1)*100, 
                                                  np.std(array_f1)))
  print('Specificity: \n Mean: {:.2f}% STD: {}'.format(np.mean(array_specificity)*100, 
                                                      np.std(array_specificity)))

  end = datetime.now()
  print('End time:', end)
  print('Duration:', end-start)


def main():
  experiment_type = sys.argv[1]

  param_grid = {
     "n_estimators" : [10,50,100,200],
     "max_features" : ["log2", "sqrt"],
     "bootstrap" : [True, False],
     "criterion": ['gini', 'entropy']
  }

  run_experiments(dataset=datasets_dict["Boatos_Lupa"],  
                  gs_flag=True,
                  hyperparameters=param_grid,
                  classifier= RandomForestClassifier(),
                  preprocessing=True,
                  vec_threshold=1,
                  feature_config=experiment_type)

  param_grid = {
        "criterion": ['gini', 'entropy'],
        "max_depth": [10,50,100,200]
  }

  run_experiments(dataset=datasets_dict["Boatos_Lupa"], 
                  gs_flag=True,
                  hyperparameters=param_grid,
                  classifier= DecisionTreeClassifier(),
                  preprocessing=True,
                  vec_threshold=1,
                  feature_config=experiment_type)

  param_grid = {
        "kernel": ['linear', 'rbf', 'sigmoid'],
        "C": [1.0,2.0,3.0,4.0]
  }

  run_experiments(dataset=datasets_dict["Boatos_Lupa"], 
                  gs_flag=True,
                  hyperparameters=param_grid,
                  classifier= SVC(),
                  preprocessing=True,
                  vec_threshold=1,
                  feature_config=experiment_type)

  param_grid = {
        "alpha": [1.0, 5.0, 10.0]
  }

  run_experiments(dataset=datasets_dict["Boatos_Lupa"], 
                  gs_flag=True,
                  hyperparameters=param_grid,
                  classifier= MultinomialNB(),
                  preprocessing=True,
                  vec_threshold=1,
                  feature_config=experiment_type)

  param_grid = {
        "n_estimators": [10,500,1000],
        "learning_rate": [0.1,0.2,0.3,0.4]
  }

  run_experiments(dataset=datasets_dict["Boatos_Lupa"], 
                  gs_flag=True,
                  hyperparameters=param_grid,
                  classifier= GradientBoostingClassifier(),
                  preprocessing=True,
                  vec_threshold=1,
                  feature_config=experiment_type)

if __name__ == "__main__":
    main()







