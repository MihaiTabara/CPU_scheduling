#! /bin/bash

MYPATH=/home/ema/Desktop/School/PDI/CPU_scheduling/log/
for I in {0..3}
do
	mkdir 192.168.6.4$I
	python util.py $MYPATH/192.168.6.4$I/stat_cpu 30 > 192.168.6.4$I/mc_prediction_cpu_30%
	python util.py $MYPATH/192.168.6.4$I/stat_cpu 50 > 192.168.6.4$I/mc_prediction_cpu_50%
	python util.py $MYPATH/192.168.6.4$I/stat_mem 30 > 192.168.6.4$I/mc_prediction_mem_30%
	python util.py $MYPATH/192.168.6.4$I/stat_mem 50 > 192.168.6.4$I/mc_prediction_mem_50%

done

mkdir server_mail_routing
python util.py $MYPATH/server_mail_routing/stat_cpu 30 > server_mail_routing/mc_prediction_cpu_30%
python util.py $MYPATH/server_mail_routing/stat_cpu 50 > server_mail_routing/mc_prediction_cpu_50%
python util.py $MYPATH/server_mail_routing/stat_mem 30 > server_mail_rounting/mc_prediction_mem_30%
python util.py $MYPATH/server_mail_routing/stat_mem 50 > server_mail_routing/mc_prediction_mem_50%

mkdir server_mail_routing
python util.py $MYPATH/server_web/stat_cpu 30 > serve_web/mc_prediction_cpu_30%
python util.py $MYPATH/server_web/stat_cpu 50 > server_web/mc_prediction_cpu_50%
python util.py $MYPATH/server_web/stat_mem 30 > server_web/mc_prediction_mem_30%
python util.py $MYPATH/server_web/stat_mem 50 > server_web/mc_prediction_mem_50% 
