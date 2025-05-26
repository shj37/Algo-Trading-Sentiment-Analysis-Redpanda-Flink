#!/bin/bash

if [ "$1" = "jobmanager" ] || [ "$1" = "taskmanager" ]; then
  exec /docker-entrypoint.sh "$@"
else
  exec "$@"
fi