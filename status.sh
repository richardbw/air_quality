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
fi

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
echo "Done."
#//EOF
