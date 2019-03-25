from configparser import ConfigParser
from itertools import chain
from queue import Queue
import threading
import subprocess
import time,os,sys
import platform




# 定义工作线程
# WORD_THREAD = 20

def product_host():
    file = 'host.conf'
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]

    host_base_list = [i.split(';')[0] for i in host_info]
    return host_base_list

def ping_ip():
    while not IP_QUEUE.empty():   # 判断队列是否为空
        ip = IP_QUEUE.get()       # 从队列中获取host数据

        local_type =  platform.system()  # 获取当前工作的系统类型

        if  local_type == 'Windows':
            command = 'ping -n 2 -w 5 %s' % ip
        elif local_type == "Linux":
            command = 'ping -c 2 -w 5 %s' % ip
        res = subprocess.call(command,shell=True,stdout=subprocess.PIPE)
        print(ip,True if res == 0 else False)

def main():
    threads = []
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=ping_ip)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    print('*****ping_test*****')
    start_time = time.time()

    test_VM_host = product_host()
    IP_QUEUE = Queue() 
    WORD_THREAD = len(test_VM_host)
    [IP_QUEUE.put(i) for i in test_VM_host]
#    with open('host_new_satus.txt','w') as f:
    main()
        
    #print('程序运行耗时：%s' % (time.time() - start_time))

