#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from functools import reduce
import numpy as np


# apply element wise operator on numpy array
def element_wise_op(array, op):
    for i in np.nditer(array,
                       op_flags=['readwrite']):
        i[...] = op(i)


class ReluActivator(object):
    def forward(self, weighted_input):
        #return weighted_input
        return max(0, weighted_input)

    def backward(self, output):
        return 1 if output > 0 else 0

class IdentityActivator(object):
    def forward(self, weighted_input):
        return weighted_input

    def backward(self, output):
        return 1


class RecurrentLayer(object):
    def __init__(self, input_width, state_width,
                 activator, learning_rate):
        self.input_width = input_width
        self.state_width = state_width
        self.activator = activator
        self.learning_rate = learning_rate
        self.times = 0       # initialise to t0 at current time step
        self.state_list = [] # save states at each time step
        self.state_list.append(np.zeros(
            (state_width, 1)))           # initialise s0
        self.U = np.random.uniform(-1e-4, 1e-4,
            (state_width, input_width))  # initialise U
        self.W = np.random.uniform(-1e-4, 1e-4,
            (state_width, state_width))  # initialise W

    def forward(self, input_array):
        '''
        perform forward calculation
        '''
        self.times += 1
        state = (np.dot(self.U, input_array) +
                 np.dot(self.W, self.state_list[-1]))
        element_wise_op(state, self.activator.forward)
        self.state_list.append(state)

    def backward(self, sensitivity_array, 
                 activator):
        '''
        implement BPTT algorithm
        '''
        self.calc_delta(sensitivity_array, activator)
        self.calc_gradient()

    def update(self):
        '''
        update weights by gradient descent
        '''
        self.W -= self.learning_rate * self.gradient

    def calc_delta(self, sensitivity_array, activator):
        self.delta_list = []  # save error at each time step
        for i in range(self.times):
            self.delta_list.append(np.zeros(
                (self.state_width, 1)))
        self.delta_list.append(sensitivity_array)
        # iteratively calculate error at each time step
        for k in range(self.times - 1, 0, -1):
            self.calc_delta_k(k, activator)

    def calc_delta_k(self, k, activator):
        '''
        calculate delta at time k by delta at time k+1
        '''
        state = self.state_list[k+1].copy()
        element_wise_op(self.state_list[k+1],
                    activator.backward)
        self.delta_list[k] = np.dot(
            np.dot(self.delta_list[k+1].T, self.W),
            np.diag(state[:,0])).T

    def calc_gradient(self):
        self.gradient_list = [] # save gradient at each time step
        for t in range(self.times + 1):
            self.gradient_list.append(np.zeros(
                (self.state_width, self.state_width)))
        for t in range(self.times, 0, -1):
            self.calc_gradient_t(t)
        # actual gradient is the sum of gradients at all times
        self.gradient = reduce(
            lambda a, b: a + b, self.gradient_list,
            self.gradient_list[0]) # [0] is initialized to 0 and has not been modified

    def calc_gradient_t(self, t):
        '''
        calculate gradient of weight at each time t
        '''
        gradient = np.dot(self.delta_list[t],
            self.state_list[t-1].T)
        self.gradient_list[t] = gradient

    def reset_state(self):
        self.times = 0       # initialise to t0 at current time step
        self.state_list = [] # save state of each time step
        self.state_list.append(np.zeros(
            (self.state_width, 1)))      # initialise s0


def data_set():
    x = [np.array([[1], [2], [3]]),
         np.array([[2], [3], [4]])]
    d = np.array([[1], [2]])
    return x, d


def gradient_check():
    # design a error function that returns the sum of all node outputs
    error_function = lambda o: o.sum()
    
    rl = RecurrentLayer(3, 2, IdentityActivator(), 1e-3)

    # calculate value of forward
    x, d = data_set()
    rl.forward(x[0])
    rl.forward(x[1])
    
    # calculate sensitivity map
    sensitivity_array = np.ones(rl.state_list[-1].shape,
                                dtype=np.float64)
    # calculate gradient using backpropagation
    rl.backward(sensitivity_array, IdentityActivator())
    
    # check if the gradient is correct
    epsilon = 10e-4
    for i in range(rl.W.shape[0]):
        for j in range(rl.W.shape[1]):
            rl.W[i,j] += epsilon
            rl.reset_state()
            rl.forward(x[0])
            rl.forward(x[1])
            err1 = error_function(rl.state_list[-1])
            rl.W[i,j] -= 2*epsilon
            rl.reset_state()
            rl.forward(x[0])
            rl.forward(x[1])
            err2 = error_function(rl.state_list[-1])
            expect_grad = (err1 - err2) / (2 * epsilon)
            rl.W[i,j] += epsilon
            print('weights(%d,%d): expected - actural %f - %f' % (
                i, j, expect_grad, rl.gradient[i,j]))


def test():
    l = RecurrentLayer(3, 2, ReluActivator(), 1e-3)
    x, d = data_set()
    l.forward(x[0])
    l.forward(x[1])
    l.backward(d, ReluActivator())
    return l


if __name__ == '__main__':
    gradient_check()
    # test()
