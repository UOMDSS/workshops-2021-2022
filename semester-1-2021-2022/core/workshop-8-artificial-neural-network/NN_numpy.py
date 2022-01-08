import numpy as np


class NeuralNetwork:
    def __init__(self, inputnodes, hiddennodes, outputnodes, learningrate):
        # number of nodes of each layer
        self.inodes = inputnodes
        self.hnodes = hiddennodes
        self.onodes = outputnodes

        # initialise weights (random distribution)
        self.wih = np.random.normal(0.0, np.power(self.hnodes, -0.5), (self.hnodes, self.inodes))
        self.who = np.random.normal(0.0, np.power(self.onodes, -0.5), (self.onodes, self.hnodes))

        # learning rate
        self.lr = learningrate

        # activation function (Sigmoid)
        self.activation_function = lambda x: 1 / (1 + np.exp(-x))

    def query(self, inputs_list):
        # input layer
        inputs = np.array(inputs_list, ndmin=2).T

        # hidden layer
        hidden_inputs = self.wih @ inputs
        hidden_outputs = self.activation_function(hidden_inputs)

        # output layer
        final_inputs = self.who @ hidden_outputs
        final_outputs = self.activation_function(final_inputs)

        return final_outputs

    def train(self, inputs_list, targets_list):
        # input layer
        inputs = np.array(inputs_list, ndmin=2).T
        targets = np.array(targets_list, ndmin=2).T

        # hidden layer
        hidden_inputs = self.wih @ inputs
        hidden_outputs = self.activation_function(hidden_inputs)

        # output layer
        final_inputs = self.who @ hidden_outputs
        final_outputs = self.activation_function(final_inputs)

        # errors used in gradient descent (different from defined loss)
        output_errors = targets - final_outputs
        hidden_errors = self.who.T @ output_errors

        # update weights (gradient descent)
        self.who -= self.lr * (-output_errors * final_outputs * (1 - final_outputs) @ hidden_outputs.T)
        self.wih -= self.lr * (-hidden_errors * hidden_outputs * (1 - hidden_outputs) @ inputs.T)


input_nodes = 784
hidden_nodes = 200
output_nodes = 10
learning_rate = 0.1

# Build Model
nn = NeuralNetwork(input_nodes, hidden_nodes, output_nodes, learning_rate)


with open('mnist_dataset/mnist_train.csv','r') as f:
    training_data_list = f.readlines()

# Train
print('Training...')
epochs = 5
for e in range(epochs):
    print('epoch', e + 1, '/', epochs)
    for t, record in enumerate(training_data_list):
        all_values = record.split(',')
        # normalise input into 0.01-0.99
        inputs = np.asfarray(all_values[1:]) / 255.0 * 0.99 + 0.01
        # generate target value (one-hot vector)
        targets = np.zeros(output_nodes) + 0.01
        targets[int(all_values[0])] = 0.99
        nn.train(inputs, targets)
        if (t + 1) % 1000 == 0:
            print('sample', str(t + 1), '/', len(training_data_list), '\r', end='')
    print()
print()


with open('mnist_dataset/mnist_test.csv', 'r') as f:
    test_data_list = f.readlines()

# Test
print('Testing...')
scorecard = []
for record in test_data_list:
    all_values = record.split(',')
    correct_label = int(all_values[0])
    inputs = np.asfarray(all_values[1:]) / 255.0 * 0.99 + 0.01
    outputs = nn.query(inputs)
    label = np.argmax(outputs)
    scorecard.append(1 if label == correct_label else 0)

# Accuracy
scorecard_array = np.asarray(scorecard)
print('Accuracy:', scorecard_array.sum() / scorecard_array.size)
