#!/bin/bash
id=`ps -h | grep -i "control.py" | awk -F ' ' 'NR==1 { print $1 }'`
kill -9 $id

