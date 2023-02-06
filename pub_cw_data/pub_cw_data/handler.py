#!/bin/bash
#
#  auth: rbw
#  date: 20230203
#  desc:
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import json
from datetime import datetime
import boto3
import logging                      #
log = logging.getLogger(__name__)   # https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
log.setLevel(logging.DEBUG)         # https://stackoverflow.com/a/8269542
 
CLOUDWATCH_NAMESPACE = "rbw/air/pollution01"
ATTRIBUTES = ["pmten", "pmtwofive"]

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event_list, context):
    log.debug("RBW> Start rbw_air_pollution_pub_cw_data--------------------------------------------------")
    log.debug("RBW> Received: event_list: %s, context: %s" %(event_list, context))

    for event in event_list:
        log.debug("RBW> event : %s" %(event)) 
        ts = int(datetime.timestamp(datetime.strptime(event['ts'], '%Y-%m-%d %H:%M:%S'))) if 'ts' in event else 0
        metric_data = []
        for key in event:
            if key in ATTRIBUTES:
                log.debug("RBW> Catching event key: %s" %(key)) 
                metric_datum = {
                    'MetricName': key,
                    'Value': event[key],
                    'Timestamp': ts

                }
                metric_data.append(metric_datum)

        print(f"Pushing /{metric_data}/ to cloudWatch {CLOUDWATCH_NAMESPACE}")
        cloudwatch.put_metric_data(MetricData=metric_data,Namespace=CLOUDWATCH_NAMESPACE) 

    log.debug("RBW>  /End rbw_air_pollution_pub_cw_data--------------------------------------------------")
    return event_list
