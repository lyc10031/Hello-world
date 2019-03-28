#!/bin/bash
# shut down ths script use kill 
id=`cat PID.txt`
echo -e " \n The process $id will be killed!!!\n"

kill -9 $id

