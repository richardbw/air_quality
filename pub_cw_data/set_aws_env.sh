#!/bin/bash
#
#  auth: rbw
#  date: 20230204
#  desc: 
#
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

export AWS_PROFILE=cli_user
unset AWS_SHARED_CREDENTIALS_FILE
unset AWS_REGION

echo "AWS_PROFILE: ${GREEN}$AWS_PROFILE ${OFF}"

#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
#//EOF
