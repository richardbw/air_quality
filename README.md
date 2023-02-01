# air_quality
Monitor air quality with RasperryPi


    $ export AWS_PROFILE=freetos_
    $ unset AWS_SHARED_CREDENTIALS_FILE
    $ unset AWS_REGION
    $ aws iotanalytics list-channels
    $ aws iotanalytics describe-channel --channel-name rbw_air_pollution01_channel

    $ aws iotanalytics list-pipelines
    $ aws iotanalytics create-pipeline   --cli-input-json file://mypipe.json
    $ aws iotanalytics describe-pipeline --pipeline-name rbw_air_pollution01_pipeline
    $ aws iam create-role --role-name rbw_air_pollution_assume --assume-role-policy-document mytrust_policy.json
    
  ---

# Links
* [Monitor air quality with a Raspberry Pi](https://www.raspberrypi.com/news/monitor-air-quality-with-a-raspberry-pi/)
* [Defra: Concentrations of particulate matter (PM10 and PM2.5)](https://www.gov.uk/government/statistics/air-quality-statistics/concentrations-of-particulate-matter-pm10-and-pm25)
* [Asthma &amp; Lung UK](https://www.blf.org.uk/taskforce/data-tracker/air-quality/pm25)

* [Troubleshooting AWS IoT Analytics](https://docs.aws.amazon.com/iotanalytics/latest/userguide/troubleshoot.html#pipeline-no-data)
* [Configure AWS IoT logging](https://docs.aws.amazon.com/iot/latest/developerguide/configure-logging.html#fine-logging-cli)
