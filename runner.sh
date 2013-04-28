#!/bin/bash

mem_generator="mem_parser.py"
mem_runner="python $mem_generator"
time_and_date='date -u'

mem_load_arg="mem_load"
cpu_load_arg="cpu_load"

print_to_file_memory_stats() {
  eval $time_and_date >> $1
  eval $mem_runner >> $1
  echo "" >> $1
}

if [ $# -eq 1 ]
then
  print_to_file_memory_stats $1
  # TODO Ema - add the cpu load function
  exit
else
  echo 'Usage: $0 $mem_load_arg $cpu_load_arg'
fi
