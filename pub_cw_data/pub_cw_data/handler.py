
import json
from datetime import datetime
import boto3
import logging                      #
log = logging.getLogger(__name__)   # https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html
log.setLevel(logging.DEBUG)         # https://stackoverflow.com/a/8269542
 
CLOUDWATCH_NAMESPACE = "rbw/air/pollution01"

cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    log.debug("RBW> Start rbw_air_pollution_pub_cw_data--------------------------------------------------")
    log.debug("RBW> Received: event: %s, context: %s" %(event, context))

    metric_data = []
    for e in event:
        metric_datum = {
            'MetricName': 'particulate',
            'Unit': 'Milliseconds', 
            'Value': int(datetime.timestamp(datetime.strptime(e['ts'], '%Y-%m-%d %H:%M:%S'))),
            'Dimensions': []
        }
        for k in e:
            metric_datum['Dimensions'].append({ 'Name': k, 'Value': str(e[k])})
        metric_data.append(metric_datum)

    print(f"Pushing /{metric_data}/ to cloudWatch {CLOUDWATCH_NAMESPACE}")
    cloudwatch.put_metric_data(MetricData=metric_data,Namespace=CLOUDWATCH_NAMESPACE) 

    log.debug("RBW>  /End rbw_air_pollution_pub_cw_data--------------------------------------------------")
    return event
