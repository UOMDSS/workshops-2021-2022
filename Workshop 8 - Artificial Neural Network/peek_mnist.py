import numpy as np
import matplotlib.pyplot as plt

def show_picture(values):  
    image_array = np.asfarray(values[1:]).reshape((28,28))
    plt.imshow(image_array, cmap='Greys', interpolation='None')
    plt.xlabel(str(values[0]))


with open('mnist_dataset/mnist_train.csv','r') as f:
    training_data_list = f.readlines()

plt.figure(figsize=(12, 6))
for i in range(1, 11):
    plt.subplot(2, 5, i)
    show_picture(training_data_list[i-1].split(','))
plt.show()
