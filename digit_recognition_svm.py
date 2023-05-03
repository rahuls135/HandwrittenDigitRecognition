# -*- coding: utf-8 -*-
"""Digit Recognition - SVM.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tVUP5kdtV5-QfrqyAPyr-L0rWCejSrZ8
"""

# Install LIBSVM
!pip install -U libsvm-official

import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from libsvm.svmutil import *
import matplotlib.pyplot as plt
import tensorflow as tf
import random
import os
import distutils
if distutils.version.LooseVersion(tf.__version__) <= '2.0':
    raise Exception('This notebook is compatible with TensorFlow 1.14 or higher, for TensorFlow 1.13 or lower please use the previous version at https://github.com/tensorflow/tpu/blob/r1.13/tools/colab/fashion_mnist.ipynb')

(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0
y_train0 = y_train
y_test0= y_test

# add empty color dimension
x_train = np.expand_dims(x_train, -1)
x_test = np.expand_dims(x_test, -1)

# Apply PCA to reduce the dimensionality of the data
nsumples, h, w, channels = x_train.shape
x_train = x_train.reshape(nsumples, h*w*channels)

nsumples, h, w, channels = x_test.shape
x_test = x_test.reshape(nsumples, h*w*channels)

# Apply LDA on dataset
lda = LDA(n_components=9)
x_train_lda = lda.fit_transform(x_train, y_train)
x_test_lda = lda.transform(x_test)

# Train an SVM classifier using LIBSVM
C = 10
gamma = 0.01
kernel_type = 2 # 0-linear. 1-polynomial. 2-radial basis. 3-sigmoid
model = svm_train(y_train, x_train_lda, f"-s 0 -t {kernel_type} -c {C} -g {gamma}")

# Evaluate the model on the testing set
p_label, p_acc, p_val = svm_predict(y_test, x_test_lda, model)