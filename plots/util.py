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
    def read_stat_file(filename, no_of_lines=-1):
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
        index = 0
        for line in lines[2:]:
            index = index + 1
            if index > int(no_of_lines):
                break
            [x, y] = line.rsplit()
            if (float(y) < min_range):
                min_range = float(y)
            if (float(y) > max_range) :
                max_range =float(y)
            X.append(float(x))
            #Y.append(int(y))
            Y.append(float(y))
            Y_int.append(y)

        return X, Y, Y_int, title, min_range, max_range

    @staticmethod
    def printGoogleCharts(X, Y, title, min_y, max_y, output):

        # Create a chart object of 750x400 pixels
        chart = SimpleLineChart(750, 400)

        # Add some data
        chart.add_data(Y)

        # Assign the labels to the pie data
#        chart.set_axis_labels(Axis.BOTTOM, X)
        chart.set_axis_labels(Axis.LEFT, range(int(min_y)-1, int(max_y)+1, 5))
        chart.set_title(title)

        # Print the chart URL
        print chart.get_url()

        # Download the chart
        chart.download(output+".png")

    @staticmethod
    def printMathplotlibCharts(X, Y, title, min_y, max_y, output):
        # Create the plot
        plt.plot(X, Y)
        plt.suptitle(title)

        # Save the figure in a separate file
        plt.savefig(output+".png")

    @staticmethod
    def create_chart(filename, type, output, no_of_lines=-1):
        X, Y, Y_int, title, min_y, max_y = util.read_stat_file(filename,
                no_of_lines)
        if type == 1:
            util.printGoogleCharts(X, Y, title, min_y, min_y, output)
        else:
            util.printMathplotlibCharts(X, Y, title, min_y, min_y, output)

if __name__ == '__main__':
    print "Saving charts"

    if len(sys.argv) < 4:
        print "Usage: ./plotting in_filename type output_file [number_of_lines]\nType: 1 - google_chart\n      2 - mathplotlib chart"
        exit(1)

    if len(sys.argv) == 4:
        util.create_chart(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        util.create_chart(sys.argv[1], int(sys.argv[2]), sys.argv[3],
                sys.argv[4])



