#!/usr/bin/env bash
export SETTING=dev

if [[ -z "$SECRET_KEY" ]]; then
  echo SECRET_KEY is empty
  exit 1

fi

echo "SECRET_KEY=$SECRET_KEY"
echo "SETTING=$SETTING"
echo "DEV_DATABASE_URL=$DEV_DATABASE_URL"

pids=$(ps -ef | grep gunicorn | grep -v "grep" | awk '{print $2}')

if [ -z "$pids" ]; then
  echo "No pids found"
else
  echo "pids=$pids"
  kill -9 $pids

fi

gunicorn main:app --reload --log-level=info

