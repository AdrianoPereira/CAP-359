import os
import numpy as np
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPool2D, Flatten, Dropout
from keras.utils import np_utils
import cv2


path = 'project/images'
ufs = os.listdir(path)
data = dict(path=[], temp=[])

for uf in ufs:
    uf = os.path.join(path, uf)
    imgs = os.listdir(uf)
    for img in imgs:
        data['path'].append(os.path.join(uf, img))
        data['temp'].append(int(img.split('__')[1]))


p25 = np.percentile(data['temp'], 25)
p50 = np.percentile(data['temp'], 50)
p75 = np.percentile(data['temp'], 75)
p100 = np.percentile(data['temp'], 100)

plt.figure(figsize=(12, 8))
plt.boxplot(pd.DataFrame(data).temp.values)
plt.text(.575, 290, "25º Percentil %s"%p25, fontdict=dict(size=16))
plt.text(.575, 285, "50º Percentil %s"%p50, fontdict=dict(size=16))
plt.text(.575, 280, "75º Percentil %s"%p75, fontdict=dict(size=16))
plt.text(.575, 275, "100º Percentil %s"%p100, fontdict=dict(size=16))
plt.xticks([])


def get_class(temp):
    if temp < p25:
        return 1
    if temp < p50:
        return 2
    if temp < p75:
        return 3

    return 4


data['class'] = [get_class(temp) for temp in data['temp']]
df = pd.DataFrame(data)


X = df.iloc[:, 0:1]
y = df.iloc[:, 2:3]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.15)

y_train = np_utils.to_categorical(y_train, num_classes=5)
y_test = np_utils.to_categorical(y_test, 5)


temp = []
for _, row in X_train.iterrows():
    temp.append(cv2.imread(row['path'], 0))
X_train = np.array(temp)

temp = []
for _, row in X_test.iterrows():
    temp.append(cv2.imread(row['path'], 0))
X_test = np.array(temp)

X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], X_test.shape[2], 1)

X_train = X_train.astype('float32')/255
X_test = X_test.astype('float32')/255

model = Sequential()
model.add(Conv2D(filters=64, kernel_size=(32, 32), input_shape=(X_train.shape[1], X_train.shape[2], 1),
                activation='relu'))
model.add(MaxPool2D(pool_size=(16, 16)))
model.add(Flatten())

model.add(Dense(units=128, activation='relu'))
model.add(Dropout(.3))
model.add(Dense(units=128, activation='relu'))
model.add(Dropout(.3))
model.add(Dense(units=5, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test))