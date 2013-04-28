#!/bin/bash

time_and_date='date -u +%D_%T'
mem_generator="mem_parser.py"
cpu_generator="cpu_parser.py"
mem_runner="python $mem_generator"
cpu_runner="python $cpu_generator"

mem_load_arg="mem_load"
cpu_load_arg="cpu_load"

print_to_file_memory_stats() {
  info=`eval $mem_runner`
  echo "$data $info" >> $1
}

print_to_file_cpu_stats() {
  eval $cpu_runner $1 $2
}

if [ $# -eq 2 ]
then
  while :
    do
      data=`eval $time_and_date`
      #echo $data
      print_to_file_memory_stats $1
      print_to_file_cpu_stats $2 $data
      sleep 5
    done
  exit
else
  echo 'Usage: $0 $mem_load_arg $cpu_load_arg'
fi
