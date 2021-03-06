# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:54:43 2020

@author: Team Mandela 
"""
# Use some functions from tensorflow_docs


from __future__ import absolute_import, division, print_function, unicode_literals

import pathlib

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn import preprocessing


import tensorflow as tf

from tensorflow import keras
from tensorflow.keras import layers

#print(tf.__version__)

path = "forestfires.csv"

dataset = pd.read_csv(path,sep=',')

#print(dataset.head())
dataset = dataset.drop(["month","day"], axis=1)
#print(dataset.head())

dataset.isna().sum()


train_dataset = dataset.sample(frac=0.8,random_state=0)
test_dataset = dataset.drop(train_dataset.index)


#sns.pairplot(train_dataset[["X", "Y", "FFMC", "DMC","ISI","temp","RH","wind","rain","area"]], diag_kind="kde")

#%%
train_labels = train_dataset.pop('area')
train_labels = np.log((train_labels + 1)) 
test_labels = test_dataset.pop('area')
test_labels= np.log((test_labels + 1))  # purposely to remove the skewness of the labe;

#print(test_labels)

# Normalize the data
max_abs_scaler = preprocessing.MaxAbsScaler()
X_train_maxabs = max_abs_scaler.fit_transform(train_dataset)
X_train = pd.DataFrame(X_train_maxabs, index=range(X_train_maxabs.shape[0]),
                          columns=range(X_train_maxabs.shape[1]))
#print((X_train_maxabs[:2]))

#%%
#build the model 1


def build_model():
  model = keras.Sequential([
    layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
    layers.Dense(128, activation='relu'),
    layers.Dense(64, activation='relu'),
    layers.Dense(1)
  ])

  optimizer = tf.keras.optimizers.RMSprop(0.001)

  model.compile(loss='mse',
                optimizer=optimizer,
                metrics=['mae', 'mse'])
  return model
    
model = build_model()
model.summary()


# test the NN

example_batch = X_train[:10]
example_result = model.predict(example_batch)
print(example_result)

##train the model
EPOCHS = 10000
print((X_train.shape))
print((train_labels.shape))
print(type(train_dataset))
print(type(X_train_maxabs))
labels= train_labels.to_numpy()
print(type(labels))
history = model.fit(X_train_maxabs, labels,epochs=EPOCHS, validation_split = 0.2, verbose=1)







