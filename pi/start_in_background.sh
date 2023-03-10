#!/bin/bash
#
#  auth: rbw
#  date: 20230131
#  desc: 
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BASE_DIR=`cd "${0%/*}/." && pwd`
PYSCRIPT="$BASE_DIR/pollution_meter-01.py"

OUTPUT_FILE="$BASE_DIR/log/nohup.out"

[ -z "$AWS_IOT_ENDPOINT" ] && echo "ERROR: envar not set: AWS_IOT_ENDPOINT" && exit 13

echo "Running $PYSCRIPT in background"
echo "Directing stdout to $OUTPUT_FILE"
echo "--------------------------------"

nohup $PYSCRIPT  &> $OUTPUT_FILE &

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
echo "Done."
#//EOF
