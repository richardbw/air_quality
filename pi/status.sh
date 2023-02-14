#!/bin/bash
#
#  auth: rbw
#  date: 20230131
#  desc: 
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BASE_DIR=`cd "${0%/*}/." && pwd`

PID=$(ps -ef | grep '[p]ython3.*pollution' | awk {'print $2'})

if [ -z "$PID" ] ; then 
    echo "Process not found"
else    
    echo "Process found: $PID"
    if [ "$1" == "kill" ] ; then
        echo "Killing $PID..."
        kill "$PID"
    fi
fi


#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
echo "Done."
#//EOF
