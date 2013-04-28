import os

os.system("ps -eo size,pid,user,command --sort -size | awk ' { hr=$1/1024 ; printf(\"%13.2f Mb \",hr) } { for ( x=4 ; x<=NF ; x++ ) { printf(\"%s \",$x) } print \"\" } ' | awk '{total=total + $1} END {print total}'")
