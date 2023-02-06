#!/usr/bin/env python3
#
#  auth: rbw
#  date: 20230127
#  desc: 
#   Thing : https://us-east-1.console.aws.amazon.com/iot/home?region=us-east-1#/thing/rbw_mypi_01
#   Policy: https://us-east-1.console.aws.amazon.com/iot/home?region=us-east-1#/policy/rbw_mypi_01-Policy
#   See also: https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import os,sys,threading,json
import serial
import coloredlogs, logging                     
from datetime import datetime
from time import sleep
from awscrt import mqtt,io
from awsiot import mqtt_connection_builder

log = logging.getLogger(__name__)               # https://coloredlogs.readthedocs.io/en/
coloredlogs.install(level='DEBUG', logger=log)  #

cert_dir        = f"{os.path.expanduser('~')}/src/python/rbw_mypi_01-certs"

aws_ca_file     = f"{cert_dir}/root-CA.crt"
aws_cert        = f"{cert_dir}/rbw_mypi_01.cert.pem"
aws_key         = f"{cert_dir}/rbw_mypi_01.private.key"
aws_endpoint    = "a22d4aoxca2zot-ats.iot.us-east-1.amazonaws.com"
aws_clientid    = f"rbw_mypi_01-{os.path.basename(__file__)}"   #current policy requires client id to be prefixed with 'rbw*'
aws_topic       = "rbw/air/pollution01"                         #current policy requires topic to be 'rbw/*'
ser             = serial.Serial('/dev/ttyUSB0')
sleep_time      = 180

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
    log.info (f"Starting "+sys.argv[0])
    log.debug (f"----------------------------------------")
    log.debug(f"CA file                  : {aws_ca_file}")
    log.debug(f"Cert file                : {aws_cert}")
    log.debug(f"Key file                 : {aws_key}")
    log.debug(f"ClientID                 : {aws_clientid}")
    log.debug(f"AWS end-point            : {aws_endpoint}")
    log.debug(f"IoT topic                : {aws_topic}")
    log.debug(f"Every                    : {sleep_time}s")
    log.debug(f"Reading from serial input: {ser}")
    log.info (f"----------------------------------------")

    try:
        mqtt_connection = connect_mqtt()

        log.info("Starting to read  (^C to stop)...")
        while True:
            data = []
            for idx in range(0, 10):
                datum = ser.read()
                data.append(datum)

            pmtwofive = int.from_bytes(b''.join(data[2:4]), byteorder='little') / 10
            pmten     = int.from_bytes(b''.join(data[4:6]), byteorder='little') / 10

            reading_json = json.dumps( {
                    'ts':           datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'), 
                    'pmtwofive':    pmtwofive, 
                    'pmten':        pmten
                }, indent=4)

            log.debug(f"Sending payload: [{reading_json}]")
            mqtt_connection.publish(
                topic   = aws_topic,
                payload = reading_json,
                qos     = mqtt.QoS.AT_LEAST_ONCE
            )
            sleep(sleep_time)

    except KeyboardInterrupt:
        log.warning("Caught ^C, and exiting")
    except:
        log.exception("Unexpected exception occurred!")

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
if __name__ == "__main__": main()
print("Done.")
#//EOF
