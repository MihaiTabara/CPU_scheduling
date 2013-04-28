#! /usr/bin/python

import re
import sys
import os

def read_cpu_file():
    """
        Reads the /proc/stat file to get the CPU load
        @ret : cpu_lists - [[user, nice, system, idle, iowait, irq, softirq]]
                            for each cpu
               total_cpu_load - [user, nice, system, idle, iowait, irq, softirqi,
                                 ctxt, processes, procs_running, procs_blocked]
               when - time info about when the command has been executed
    """

    total_cpu_load = []
    cpu_lists = []

    fd = open ("/proc/stat", "r")
    content = fd.readlines()
    fd.close()

    # Get the total cpu_load
    search_item_regex = '(?P<search_item>(\d+( )*)+)'
    cpu_regex = 'cpu\d*( )+'+ search_item_regex
    sys_regex = '(ctxt|processes|procs_running|procs_blocked)( )+'+ search_item_regex

    for line in content:
        m = re.search(cpu_regex, line)

        if m:
            if 'cpu ' in line:
                total_cpu_load = m.group('search_item').rsplit()[:7]
            else:
                cpu_lists.append(m.group('search_item').rsplit()[:7])
        else:
            m = re.search(sys_regex, line)

            if not m:
                continue
            total_cpu_load.append(m.group('search_item'))

    return total_cpu_load, cpu_lists

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print "Usage: ./cpu_parser.py out_file time"

    total_cpu_load, cpu_list = read_cpu_file()
    endl = '\n'

    # print general statistics
    fd = open(sys.argv[1], "a")
    fd.write(sys.argv[2] + ' ' + ' '.join(total_cpu_load) + endl)
    fd.close()

    # print statistics per CPU
    for cpu in cpu_list:
        fd = open(sys.argv[1]+str(cpu_list.index(cpu)), "a")
        fd.write(sys.argv[2] + ' ' + ' '.join(cpu) + endl)
        fd.close()
