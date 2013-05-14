#! /usr/bin/python

from pygooglechart import SimpleLineChart
from pygooglechart import Axis
import sys
import matplotlib.pyplot as plt

class util:
    @staticmethod
    def read_cpu_file(filename):
        """
            @Ret value: ret_value - vector
            ret_value format:
                * [date, data]
        """

        ret_value = []

        fd = open(filename, "r")
        fd.close()

    @staticmethod
    def read_mem_file(filename):
        """
            @Ret value: ret_value - vector
            ret_value format:
                * [date, data]
        """

        ret_value = []

        fd = open(filename, "r")
        fd.close()

    @staticmethod
    def read_stat_file(filename):
        """
            Method that reads prediction data
            @Ret value: X = [x1, x2, ..]
                        Y = [y1, y2, ..]
                        name = title of the chart
        """
        # X - X axis of the chart
        X = []
        # Y - Y axis of the chart
        Y = []
        Y_int = []

        fd = open(filename, "r")
        lines = fd.readlines()
        fd.close()


        # Get the number of (x, y) pairs
        N = int(lines[0])
        # And the title of the chart
        title = lines[1]

        # Read (x, y) pairs
        max_range = -100
        min_range = 9999999999
        for line in lines[2:]:
            [x, y] = line.rsplit()
            if (int(y) < min_range):
                min_range = int(y)
            if (int(y) > max_range) :
                max_range = int(y)
            X.append(int(x))
            #Y.append(int(y))
            Y.append(int(y))
            Y_int.append(y)

        return X, Y, Y_int, title, min_range, max_range

    @staticmethod
    def printGoogleCharts(X, Y, title, min_y, max_y):

        # Create a chart object of 750x400 pixels
        chart = SimpleLineChart(750, 400)

        # Add some data
        chart.add_data(Y)

        # Assign the labels to the pie data
#        chart.set_axis_labels(Axis.BOTTOM, X)
        chart.set_axis_labels(Axis.LEFT, range(min_y, max_y, 5))
        chart.set_title(title)

        # Print the chart URL
        print chart.get_url()

        # Download the chart
        chart.download(title+".png")

    @staticmethod
    def printMathplotlibCharts(X, Y, title, min_y, max_y):
        # Create the plot
        plt.plot(X, Y)
        plt.suptitle(title)

        # Save the figure in a separate file
        plt.savefig(title+".png")

    @staticmethod
    def create_chart(filename, type):
        X, Y, Y_int, title, min_y, max_y = util.read_stat_file(filename)
        if type == 1:
            util.printGoogleCharts(X, Y, title, min_y, min_y)
        else:
            util.printMathplotlibCharts(X, Y, title, min_y, min_y)



if __name__ == '__main__':
    print "Saving charts"


    if len(sys.argv) < 3:
        print "Usage: ./plotting in_filename type\nType: 1 - google_chart\n      2 - mathplotlib chart"
        exit(1)

    util.create_chart(sys.argv[1], int(sys.argv[2]))


