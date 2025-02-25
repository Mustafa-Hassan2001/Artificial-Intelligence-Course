# -*- coding: utf-8 -*-
"""Graded_task_08b_Neural_Networks_AM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/13EXNnAyN6od3gqIxfUbGHEBkyJfer1Tr

Load the Diabetes Dataset.



```
from keras.datasets import fashion_mnist

fashion_mnist.load_data()

```
"""

from keras.datasets import fashion_mnist

(X_train, y_train), (X_test, y_test) = fashion_mnist.load_data()

"""Import Libraries

```
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras import optimizers
```


"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Flatten
from keras.utils import to_categorical
from keras import optimizers

"""Split Dataset"""

X_train = X_train / 255.0
X_test = X_test / 255.0

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

"""Model creation"""

model = Sequential()

"""Layers Addition

```
No. of epochs = 100
Hidden unit = 100
batch size = length of training input

```


"""

model.add(Flatten(input_shape=(28, 28)))

model.add(Dense(100, activation='relu'))

model.add(Dense(10, activation='softmax'))

"""Compilation"""

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

"""Fitting the model"""

history = model.fit(X_train, y_train, epochs=100, batch_size=len(X_train), validation_data=(X_val, y_val), verbose=2)

"""Draw the Training and validation loss"""

plt.plot(history.history['loss'], label='Training loss')
plt.plot(history.history['val_loss'], label='Validation loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.title('Training and Validation Loss')
plt.show()

