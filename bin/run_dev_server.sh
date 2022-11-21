#!/usr/bin/env bash
export SETTING=dev
export DEV_DATABASE_URL=postgres://snemjqmwzxqtgy:b2d4c7f51b6ae77dc64ce67d05ec1fefeed4b4ee3d397f9add2047525283de36@ec2-18-215-41-121.compute-1.amazonaws.com:5432/dpfbv163nkor3

if [[ -z "$SECRET_KEY" ]]; then
  echo "$SECRET_KEY" is empty
  exit 1

fi

echo "SECRET_KEY=$SECRET_KEY"
echo "SETTING=$SETTING"
echo "DEV_DATABASE_URL=$DEV_DATABASE_URL"

gunicorn main:app --reload --log-level=info

