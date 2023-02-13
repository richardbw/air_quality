#!/bin/bash
#
#  auth: rbw
#  date: 20230203
#  desc:
#
#   When called by TopicRule, there's one event at a time; a Channel sends a list of events
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import json
from datetime import datetime
import boto3
import logging                      #
log = logging.getLogger(__name__)   # https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
log.setLevel(logging.DEBUG)         # https://stackoverflow.com/a/8269542
 
POL_CLOUDWATCH_NAMESPACE = "rbw/air/pollution01"
POL_ATTRIBUTES = ["pmten", "pmtwofive"]

HUM_CLOUDWATCH_NAMESPACE = "rbw/air/temphumid01"
HUM_ATTRIBUTES = ["humidity", "temp", "pressure"]

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    log.debug("RBW> Start rbw_air_pub_cw_data--------------------------------------------------")
    log.debug("RBW> Received: event: %s, context: %s" %(event, context))

    if   all(key in event for key in HUM_ATTRIBUTES) :
        namespace = HUM_CLOUDWATCH_NAMESPACE
        attributes = HUM_ATTRIBUTES
    elif all(key in event for key in POL_ATTRIBUTES) : 
        namespace = POL_CLOUDWATCH_NAMESPACE
        attributes = POL_ATTRIBUTES
    else:
        log.warn("RBW> Event missing recognised keys : %s" %(event)) 
        return event

    metric_data = []
    ts = int(datetime.timestamp(datetime.strptime(event['ts'], '%Y-%m-%d %H:%M:%S'))) if 'ts' in event else 0

    for key in event:
        if key == 'ts': continue
        if key not in attributes: continue

        log.debug(f"RBW> datum> {key:15} : {event[key]}")

        #NBNBNB: all cloudwatch Values must be ints/floats (!strings)
        metric_datum = {
            'MetricName': key,
            'Value': event[key],
            'Timestamp': ts
        }
        metric_data.append(metric_datum)

    print(f"Pushing /{metric_data}/ to cloudWatch namespace: {namespace}")
    cloudwatch.put_metric_data(MetricData=metric_data,Namespace=namespace) 

    log.debug("RBW>  /End rbw_air_pub_cw_data--------------------------------------------------")
    return event
