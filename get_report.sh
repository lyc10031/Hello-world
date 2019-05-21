#!/bin/bash
#usage：
#     ./get_report              ## read run_result 
#     or
#     ./get_report result-1     ## read result-1
if [ ! -d "run_result" ];then
echo "run_result did not exit !!!"
exit 2
fi

if [ $# == 1 ];then
for i in `ls $1/*.txt`
do
awk -F ' ' '{print $4,"<->",$5,$6 }' $i  | grep OK | tail -n 1
done

else

for i in `ls run_result/*.txt`
do
awk -F ' ' '{print $4,"<->",$5,$6 }' $i  | grep OK | tail -n 1
done
fi
