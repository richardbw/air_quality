#!/usr/bin/env python3
#
#  auth: rbw
#  date: 20230127
#  desc: 
#   Thing : https://us-east-1.console.aws.amazon.com/iot/home?region=us-east-1#/thing/rbw_mypi_01
#   Policy: https://us-east-1.console.aws.amazon.com/iot/home?region=us-east-1#/policy/rbw_mypi_01-Policy
#   See also: https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os,sys,json,argparse
import coloredlogs, logging                     
from datetime import datetime
from time import sleep
from sds011 import SDS011
from awscrt import mqtt,io
from awsiot import mqtt_connection_builder

log = logging.getLogger(__name__)               # https://coloredlogs.readthedocs.io/en/
coloredlogs.install(level='DEBUG', logger=log)  #

aws_topic       = "rbw/air/pollution01"                         #current policy requires topic to be 'rbw/*'
aws_clientid    = f"rbw_mypi_01-{os.path.basename(__file__)}"   #current policy requires client id to be prefixed with 'rbw*'
CERT_DIR        = f"{os.path.expanduser('~')}/src/python/rbw_mypi_01-certs"
SERIAL_PORT     = '/dev/ttyUSB0'
PUBLISH_TO_AWS  = True 
USE_SDS011 = True 
SLEEP_TIME      = 180



def cmd_args(): #{{{
    global USE_SDS011, PUBLISH_TO_AWS, SLEEP_TIME, CERT_DIR
    parser = argparse.ArgumentParser(
        prog        = 'Particulate Stat Monitor',  
        description = 'Publish particulate stats to MQTT/AWS',
        epilog      = '---'
    )
    parser.add_argument('-s',   dest='use_sds011',      help='Switch OFF serial port - for non-Pi execution', action=argparse.BooleanOptionalAction )
    parser.add_argument('-a',   dest='publish_to_aws',  help='Switch OFF publishing to AWS',                  action=argparse.BooleanOptionalAction )
    parser.add_argument('-t',   dest='sleep_time',      help=f'Set polling/sleep time; default is {SLEEP_TIME}s', default=SLEEP_TIME)
    parser.add_argument('-c',   dest='cert_dir',        help=f'Override certificate directory; default is {CERT_DIR}s', default=CERT_DIR)
    args = parser.parse_args()

    USE_SDS011      = not args.use_sds011
    PUBLISH_TO_AWS  = not args.publish_to_aws
    SLEEP_TIME      = int(args.sleep_time)
    CERT_DIR        = args.cert_dir

    if PUBLISH_TO_AWS and not 'AWS_IOT_ENDPOINT' in os.environ: 
        log.error(f"No environment variable set for AWS_IOT_ENDPOINT")
        sys.exit(24)
#}}}


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# partially taken from ~/src/python/aws-iot-device-sdk-python-v2/samples/pubsub.py

def on_connection_interrupted(connection, error, **kwargs):
    log.error("Connection interrupted. error: {}".format(error))

# Callback when an interrupted connection is re-established.
def on_connection_resumed(connection, return_code, session_present, **kwargs):
    log.info("Connection resumed. return_code: {} session_present: {}".format(return_code, session_present))

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
def connect_mqtt(): #{{{
    aws_ca_file     = f"{CERT_DIR}/root-CA.crt"
    aws_cert        = f"{CERT_DIR}/rbw_mypi_01.cert.pem"
    aws_key         = f"{CERT_DIR}/rbw_mypi_01.private.key"
    aws_endpoint    = os.environ['AWS_IOT_ENDPOINT']
    log.debug (f"----------------------------------------")
    log.debug(f"CA file                  : {aws_ca_file}")
    log.debug(f"Cert file                : {aws_cert}")
    log.debug(f"Key file                 : {aws_key}")
    log.debug(f"ClientID                 : {aws_clientid}")
    log.debug(f"AWS end-point            : {aws_endpoint}")
    log.debug(f"IoT topic                : {aws_topic}")
    log.info (f"----------------------------------------")

    if not os.path.isfile(aws_cert):
        log.error(f"File not found: {aws_cert}")
        sys.exit(81)

    event_loop_group = io.EventLoopGroup(1)
    client_bootstrap = io.ClientBootstrap(event_loop_group, io.DefaultHostResolver(event_loop_group))
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint            = aws_endpoint,
        cert_filepath       = aws_cert,
        pri_key_filepath    = aws_key,
        ca_filepath         = aws_ca_file,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id           = aws_clientid,
        client_bootstrap    = client_bootstrap,
        clean_session       = False,
        keep_alive_secs     = 30
    )
    log.info(f"Connecting to {aws_endpoint} with client ID '{aws_clientid}'...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    log.info("Connected!")
    return mqtt_connection
#}}}






def main():
    cmd_args()

    if USE_SDS011:
        sds = SDS011(port=SERIAL_PORT, rate=5)
        log.debug(f"Reading from SDS:\n{sds}")

    log.info (f"Starting "+sys.argv[0])

    try:
        if PUBLISH_TO_AWS:
            mqtt_connection = connect_mqtt()

        log.info(f"Starting to read every {SLEEP_TIME}s (^C to stop)...")
        while True:
            m = sds.read_measurement() if USE_SDS011 else {'timestamp': datetime.utcnow(), 'pm2.5':0, 'pm10':0}

            reading_json = json.dumps( {
                    'ts':           datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                    'timestamp':    m['timestamp'].strftime('%Y-%m-%d %H:%M:%S'),
                    'pmtwofive':    m['pm2.5'], 
                    'pmten':        m['pm10']
                }, indent=4)
        
            if PUBLISH_TO_AWS:
                log.debug(f"Sending payload: [{reading_json}]")
                mqtt_connection.publish(
                    topic   = aws_topic,
                    payload = reading_json,
                    qos     = mqtt.QoS.AT_LEAST_ONCE
                )
            else:
                log.debug(f"Serial reading: [{reading_json}]")

            sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        log.warning("Caught ^C, and exiting")
    except:
        log.exception("Unexpected exception occurred!")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__": main()
print("Done.")
#//EOF
