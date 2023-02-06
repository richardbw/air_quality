#!/bin/bash
#
#  auth: rbw
#  date: 20230204
#  desc: 
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

unset AWS_SHARED_CREDENTIALS_FILE
export AWS_PROFILE=cli_user
export AWS_REGION=us-east-1

echo "AWS_PROFILE: ${GREEN}$AWS_PROFILE ${OFF}"
echo "AWS_REGION:  ${GREEN}$AWS_REGION ${OFF}"

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#//EOF
