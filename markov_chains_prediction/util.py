#! /usr/bin/python

import sys
import random

class Constants:

    MEM_FILE = 1
    CPU_FILE = 2
    MAXIMUM = 99999999999.0
    MINIMUM = -1

class Reader:

    """
        Internal values:
            filename - filename to be read
            raw_values - vector with computed
                        diffs
            time_values - time_vector
            min_value/max_value - extreme values from files
    """

    def __init__(self, filename, f_type, percent):
        self.f_type = type
        self.filename = filename
        self.percentage = percent

    def read_file(self, filename=None):

        if not filename:
            fd = open(self.filename, "r")
        else:
            fd = open(filename, "r")

        values = fd.readlines()

        self.raw_values = []
        self.time_values = []


        self.time_values.append(values[0].rsplit()[0].rsplit('_')[-1])

        if self.f_type == Constants.MEM_FILE:
            init_value = float(values[0].rsplit()[-1])
        else:
            aux = values[0].rsplit()[1:4]
            init_value = float(aux[0]) + float(aux [1])+ float(aux[2])

        self.min_val = Constants.MAXIMUM
        self.max_val = Constants.MINIMUM

        for val in values[1:]:
            if self.f_type == Constants.MEM_FILE:
                current_value = val.rsplit()[-1]
            else:
                aux = val.rsplit()[1:4]
                current_value = float(aux[0]) + float(aux [1])+ float(aux[2]) 

            self.time_values.append(val.rsplit()[0].rsplit('_')[-1])
            aux = float(current_value - init_value)
            self.raw_values.append(aux)

            if self.min_val > aux:
                self.min_val = aux
            if self.max_val < aux:
                self.max_val = aux

            init_value = current_value

class SimpleMarkovChains:

    def __init__(self, reader):
        self.r = reader
        self.trans_matrix = []
        self.state = []

        """
            Transition matrix is the matrix that states the
            probability for the system to switch from state i
            to state j
            Gathered through sampling
        """
        for i in range(0,self.r.max_value + 1):
            aux = []
            for j in range(0,self.r.max_value + 1):
                aux.append(float(0))
            self.trans_matrix.append(aux)

        for i in range(0, self.r.max_value + 1):
            self.state.append(0)

    def train_states(self, percent=None):

        if not percent:
            self.max_index = self.r.percent*len(self.r.raw_values)/100
        else:
            self.max_index = percent*len(self.r.raw_values)/100

        self.state[self.r.raw_values[0]] += 1

        for i in range(1,self.max_index):
            prev = self.r.raw_values[i-1]
            cur = self.r.raw_values[i]
            self.state[cur] += 1
            self.trans_matrix[prev][cur] += 1

        for i in range(0,len(self.trans_matrix)):
            for j in range(0, len(self.trans_matrix)):
                self.trans_matrix[i][j] = self.trans_matrix[i][i] / self.max_index

        for i in range(0, len(self.state)):
            self.state[i] /= self.max_index


    def get_next_state(self, curent_state, trans_matrix):

        result = []

        for i in range(0, self.r.min_val):
            result.append(0)

        for i in range(self.r.min_val, self.r.max_val+1):
            value = 0
            for j in range(self.r.min_value, self.r.max_value+1):
                value += curent_state[j]*trans_matrix[j][i]
            result.append(value)

        return result

    def update_current_state(self, value):
        """
        """
        # Update current_state
        self.state[value] += 1

        # Update transition matrix
        for i in range(self.r.min_value, self.r.max_value + 1):
            for j in range(self.r.min_value, self.r.max_value + 1):
                aux = self.trans_matrix[i][j]
                if j == value:
                    self.trans_matrix[i][j] = (aux * self.max_index + 1)/ (self.max_index + 1)
                else:
                    self.trans_matrix[i][j] = (aux * self.max_index)/(self.max_index + 1)

        self.max_index += 1

    def predict(self, no_of_steps, percentage=None):
        self.train_states()

        for i in range(0, no_of_steps):
            result = self.get_next_state(self.state, self.trans_matrix)
            # TODO Map results to intervals
            # Be carefull at the following scenario:
            # [ 0 0 0 0 13 1 13 1 13 42 ]
            value = 23242
            # Update current state
            self.update_current_state(value)

if __name__ == '__main__':
    print "starting...\n"

    if len(sys.argv) < 3:
        print "Usage: %s in_file percent" %sys.argv[0]
        exit(1)

    if 'cpu' in sys.argv[1]:
        my_r = Reader(sys.argv[1], Constants.CPU_FILE, percent)
    elif 'mem' in sys.argv[1]:
        my_r = Reader(sys.argv[1], Constants.MEM_FILE, percent)

    my_r.read_file()

