#!/bin/bash
cd /home/pi/lvyuan_solar_control
/usr/bin/python3 /home/pi/lvyuan_solar_control/main.py --daily-report >> /home/pi/lvyuan_solar_control/logs/direct_run.log 2>&1

