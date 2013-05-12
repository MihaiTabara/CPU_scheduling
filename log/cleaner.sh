#! /bin/bash

MYPATH=`pwd`
for I in {0..3}
do
	cd $MYPATH/CPU_scheduling@192.168.6.4$I
	echo `pwd`
	rm -f CPULoadPrediction.*
	rm -f *.py
	rm -f runner.sh
	rm -f README.md
	rm -rf .git
	#mv stats/* .
	#rm -rf stats
	new_folder=`pwd | cut -d'/' -f9 | cut -d'@' -f2`
	echo path = $new_folder
	cd $MYPATH
	mkdir $new_folder
	cp CPU_scheduling@192.168.6.4$I/stat_* $new_folder

done
