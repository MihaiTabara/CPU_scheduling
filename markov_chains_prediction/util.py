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
            min_val/max_val - extreme values from files
    """

    def __init__(self, filename, f_type, percent):
        self.f_type = f_type
        self.filename = filename
        self.percentage = float(percent)

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
                current_value = float(val.rsplit()[-1])
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

    def __init__(self, reader, percent=None):
        self.r = reader
        self.trans_matrix = []
        self.state = []

        self.encode_states()

        if not percent:
            self.max_index = int(self.r.percentage*len(self.r.raw_values)/100)
        else:
            self.max_index = int(percent*len(self.r.raw_values)/100)

        self.test_chunk_size = len(self.r.raw_values) - self.max_index 

        """
            Transition matrix is the matrix that states the
            probability for the system to switch from state i
            to state j
            Gathered through sampling
        """

        for i in range(0,len(self.state_mapping)):
            aux = []
            for j in range(0, len(self.state_mapping)):
                aux.append(float(0))
            self.trans_matrix.append(aux)

        for i in range(0, len(self.state_mapping)):
            self.state.append(0.0)

    def encode_states(self):
        self.state_mapping = {}

        for el in self.r.raw_values:
            if el in self.state_mapping.values():
                continue
            else:
                value = len(self.state_mapping)
                self.state_mapping[value] = el

    def get_dict_key_for_value(self, value):
        for key in self.state_mapping.keys():
            if self.state_mapping[key] == value:
                return key
        return -1

    def train_states(self, percent):

        #if not percent:
        #    self.max_index = int(self.r.percentage*len(self.r.raw_values)/100)
        #else:
        #    self.max_index = int(percent*len(self.r.raw_values)/100)

        #self.test_chunk_size = len(self.r.raw_values) - self.max_index

        self.state[self.get_dict_key_for_value(self.r.raw_values[0])] += 1

        for i in range(1,self.max_index):
            prev = self.r.raw_values[i-1]
            cur = self.r.raw_values[i]
            i_ind = self.get_dict_key_for_value(cur)
            j_ind = self.get_dict_key_for_value(prev)
            self.state[i_ind] += 1
            self.trans_matrix[j_ind][i_ind] += 1

        for i in range(0,len(self.trans_matrix)):
            for j in range(0, len(self.trans_matrix)):
                self.trans_matrix[i][j] /= self.max_index

        for i in range(0, len(self.state)):
            self.state[i] /= self.max_index


    def get_next_state(self, curent_state, trans_matrix):

        result = []

        for i in range(0, len(self.trans_matrix)):
            value = 0
            for j in range(0, len(self.trans_matrix)):
                value += curent_state[j]*trans_matrix[j][i]
            result.append(value)

        return result

    def update_current_state(self, value):
        """
        """
        # Update current_state
        for i in range(0, len(self.state)):
            if self.state[i] == value:
                self.state[i] = (self.state[i]*self.max_index + 1)/ (self.max_index+1)
            else:
                self.state[i] = (self.state[i]* self.max_index) / (self.max_index + 1)

        # Update transition matrix
        for i in range(0, len(self.trans_matrix)):
            for j in range(0, len(self.trans_matrix)):
                aux = self.trans_matrix[i][j]
                if j == value:
                    self.trans_matrix[i][j] = (aux * self.max_index + 1)/ (self.max_index + 1)
                else:
                    self.trans_matrix[i][j] = (aux * self.max_index)/(self.max_index + 1)


        self.max_index += 1

    def get_predicted_value(self, result):

        mapping = [0]
        j = 0
        for i in range(0, len(self.trans_matrix)):
            if result[i] == 0:
                mapping.append(mapping[j]+0.00000000000000001)
            else:
                mapping.append(mapping[j]+result[i])
            j += 1

        rand_number = random.uniform(0, mapping[-1])

        # Search result in mapping
        from util import search_float
        return search_float(rand_number, mapping)

    def predict(self, no_of_steps, percentage=None):
        self.train_states(percentage)

        for i in range(0, no_of_steps):
            result = self.get_next_state(self.state, self.trans_matrix)
            # Map results to intervals
            value = self.get_predicted_value(result)
            print "%s\t%s"%(self.r.time_values[self.max_index+1],
                    self.state_mapping[value])
            # Update current state
            self.update_current_state(value)

#@staticmethod
def search_float(value, where, start=None, finish=None):

    if not start:
        left = 0
    else:
        left = start
    if not finish:
        right = len(where)
    else:
        right = finish
    if value == 0:
        return start
    while 1:
        if right <= left:
            return -1
        index = (left+right)/2
        if value > where[index - 1] and value <= where[index]:
            return index - 1
        if value > where[index] and value <= where[index + 1]:
            return index
        if value == where[index]:
            return index - 1
        if (value < where[index]):
            right = index - 1
        if (value > where[index]):
            left = index + 1

def read_stat_file(filename):
        """
            Method that reads prediction data
                        Y = [y1, y2, ..]
        """
        # Y - Y axis of the chart
        Y = []

        fd = open(filename, "r")
        lines = fd.readlines()
        fd.close()

        # Read (x, y) pairs
        for line in lines[2:]:
            [x, y] = line.rsplit()
            #Y.append(int(y))
            Y.append(float(y))

        return Y

def compare_results(result_vector, real_vector, percentage, time_values):

    start_index = int(percentage*len(real_vector)/100) + 1
    i = 0

    for j in range (start_index, len(real_vector)):
        print "%s\t%s"%(time_values[j], float(result_vector[i] - real_vector[j]))
        i += 1

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print "Usage: %s in_file percent [prediction_file]" %sys.argv[0]
        exit(1)

    if 'cpu' in sys.argv[1]:
        reader = Reader(sys.argv[1], Constants.CPU_FILE, sys.argv[2])
        print 12
        print "Markov Chains - Error CPU file %s train_set"%sys.argv[2]
    elif 'mem' in sys.argv[1]:
        reader = Reader(sys.argv[1], Constants.MEM_FILE, sys.argv[2])
        print 12
        print "Markov Chains - Error Memory file %s train_set"%sys.argv[2]

    reader.read_file()
    #print reader.raw_values
    mc = SimpleMarkovChains(reader)

    if len(sys.argv) == 4:
        predicted_vector = read_stat_file(sys.argv[3])
        compare_results(predicted_vector, reader.raw_values, float(sys.argv[2]), reader.time_values)
    else:
        mc.predict(mc.test_chunk_size)
