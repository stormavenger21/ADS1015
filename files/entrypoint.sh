#!/bin/sh

set -e

echo "Starting ADS1015 driver"

cd /ADS1015/app
/opt/venv/bin/python -u -m app &

echo "Starting Nginx..."
exec nginx -g "daemon off;"
