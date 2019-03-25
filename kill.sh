#!/bin/bash
# shut down ths script use kill 
id=`ps -h | grep -i "control.py" | awk -F ' ' 'NR==1 { print $1 }'`
kill -9 $id

