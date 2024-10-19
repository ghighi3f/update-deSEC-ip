#!/bin/bash

set -e

exec python3 bot.py &
exec python3 check_and_change_dns.py &
exec python3 thermostat.py