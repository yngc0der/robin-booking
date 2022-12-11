#!/bin/sh

set -e

if [ "$1" = "run" ]; then
    exec /usr/local/bin/supercronic /usr/src/app/crontab
fi

exec "$@"
