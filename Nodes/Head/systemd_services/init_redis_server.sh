#!/bin/bash
source /home/cosmic/anaconda3/bin/activate /home/cosmic/anaconda3/envs/cosmic_vla

workdir="/home/cosmic/dev/logs"
logstem="${workdir}/redis_server"

export PYTHONUBUFFERED=yes

echo "Starting redis_server"

if test -f "$logstem.out"; then
	echo "Trimming log $logstem.out"
	tail -n 100000 $logstem.out > tmp.out
	mv -f tmp.out $logstem.out
	echo -------------------- >> $logstem.out
	echo Startup `date` >> $logstem.out
fi
if test -f "$logstem.err"; then
	echo "Trimming log $logstem.err"
	tail -n 100000 $logstem.err > tmp.err
	mv -f tmp.err $logstem.err
	echo -------------------- >> $logstem.err
	echo Startup `date` >> $logstem.err
fi

/home/cosmic/anaconda3/envs/cosmic_vla/bin/redis-server --protected-mode no < /dev/null 1>> "${logstem}.out" 2>> "${logstem}.err"