#!/bin/bash
#
#  auth: rbw
#  date: 20230309
#  desc: 
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
BASE_DIR=`cd "${0%/*}/." && pwd`

cat <<EOT > /dev/stderr
WIP WIP WIP
EOT

CW_NS_PAR='rbw/air/pollution01'
CW_NS_HUM='rbw/air/temphumid01'

METRIC='pmten'
STATISTICS='SampleCount Average Sum Minimum Maximum'

start_time=$(date -v -7d  '+%Y-%m-%dT%H:%M:%S')
now=$(date '+%Y-%m-%dT%H:%M:%S')


cat <<EOT > /dev/stderr
Metrics for :   $CW_NS_PAR
metric      :   $METRIC  
from        :   $start_time
to          :   $now
stats       :   $STATISTICS
EOT

echo "Timestamp $STATISTICS" | sed 's/ /,/g'
aws cloudwatch get-metric-statistics                    \
    --namespace $CW_NS_PAR                              \
    --metric-name $METRIC                               \
    --statistics $STATISTICS                            \
    --period 3600                                       \
    --start-time $start_time                            \
    --end-time $now                                     \
| jq -r ".Datapoints[] | [.Timestamp, .$(echo $STATISTICS | sed 's/ /, ./g')] | @csv"
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
echo "Done." > /dev/stderr
#//EOF
