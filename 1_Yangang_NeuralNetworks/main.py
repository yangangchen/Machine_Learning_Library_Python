# main.py
#
# Author: Yangang Chen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# 
# Implementation of feed forward deep neural networks.
# ==============================================================================

import numpy as np
import h5py
import matplotlib.pyplot as plt
from NN import *

np.random.seed(1)
np.set_printoptions(precision=4, threshold=np.inf, linewidth=np.inf, suppress=True)


def load_data():
    train_dataset = h5py.File('datasets/train_catvnoncat.h5', "r")
    train_x = np.array(train_dataset["train_set_x"][:])  # your train set features
    train_y = np.array(train_dataset["train_set_y"][:])  # your train set labels

    test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
    test_x = np.array(test_dataset["test_set_x"][:])  # your test set features
    test_y = np.array(test_dataset["test_set_y"][:])  # your test set labels

    classes = np.array(test_dataset["list_classes"][:])  # the list of classes

    train_x = train_x.reshape((train_x.shape[0], -1)) / 255.
    test_x = test_x.reshape((test_x.shape[0], -1)) / 255.
    train_y = np.expand_dims(train_y, axis=1)
    test_y = np.expand_dims(test_y, axis=1)

    return train_x, train_y, test_x, test_y, classes


def main():
    train_x, train_y, test_x, test_y, classes = load_data()
    # print(train_x.shape)  # (209, 12288)
    # print(train_y.shape)  # (209, 1)
    # print(test_x.shape)  # (50, 12288)
    # print(test_y.shape)  # (50, 1)

    NN = NeuralNetwork(learning_task='classification-two-classes',
                       dim_layers=[12288, 20, 7, 5, 1])

    score = NN.evaluate_accuracy(train_x, train_y)
    print("Training accuracy (before training) is: " + str(score))

    step_array = []
    loss_array = []

    for step in range(3000 + 1):
        loss = NN.train_onestep(train_x, train_y, 0.01)

        if step % 100 == 0:
            print("step: " + str(step) + ", loss: " + str(loss))
            step_array.append(step)
            loss_array.append(loss)

    # print([i for i in NN.parameters])
    # print([NN.parameters[i].shape for i in NN.parameters])
    # print([i for i in NN.cache])
    # print([NN.cache[i].shape for i in NN.cache])

    fig = plt.figure()
    plt.plot(np.array(step_array), np.array(loss_array))
    plt.show()
    fig.savefig('training_loss.png', bbox_inches='tight')
    plt.close(fig)

    score = NN.evaluate_accuracy(train_x, train_y)
    print("Training accuracy (after training) is: " + str(score))

    score = NN.evaluate_accuracy(test_x, test_y)
    print("Test accuracy is: " + str(score))


if __name__ == '__main__':
    main()
