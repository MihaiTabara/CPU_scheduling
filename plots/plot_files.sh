#! /bin/bash

PLOTTER=util.py
NO_OF_LINES=200

function plot_data() {
	for file in `find $1 ! -name "*.png" | tr ' ' '\n'`
	do
		if [ -d $file ]
		then
			continue
		fi
		fname=`echo $file | cut -d'/' -f 3`
		echo Plotting data from $file
		python $PLOTTER $file $2 $1/plots/$fname $NO_OF_LINES
	done
}

# USAGE: ./plot_data input folder, type of chart (google or matplotlib)

# Tendency based predictors
plot_data tendency_component/192\.168\.6\.40 2
plot_data tendency_component/192\.168\.6\.41 2
plot_data tendency_component/192\.168\.6\.42 2
plot_data tendency_component/192\.168\.6\.43 2

# TODO - Add the other 2 data sets
