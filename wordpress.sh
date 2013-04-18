#!/bin/bash

# This script works as cron, bcoz I dont have access to cronjob on pulse7

while true
do
  python main.py > /dev/null &
	sleep 43200
done

