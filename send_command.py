import paramiko
import time,sys
from configparser import ConfigParser
import subprocess
import platform
from queue import Queue
from itertools import chain
import threading
import os


IP_QUEUE = Queue()

def ping_ip(ip):

    local_type =  platform.system()

    if local_type == 'Windows':
        command = 'ping -n 3 -w 5 %s' % ip
    elif local_type == "Linux":
        command = 'ping -c 3 -w 5 %s' % ip

    res = subprocess.call(command,shell=True,stdout=subprocess.PIPE)
    # 打印运行结果
    # print(ip,True if res == 0 else False ,file = f )

    # print(ip,True if res == 0 else False)
    return True if res == 0 else False

def record_host_status(name,info):
    """ 获取记录结果 写入文件中 """
    try:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
    except:
        pass
    with open(f'tmp/{name}_status.txt','a+') as s:
        tt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        s.write(f'{tt} <--* {info} *--> times\n')

def send_command():
    host_info = IP_QUEUE.get()
    host,port,username,password = split_host_info(host_info)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    host_mark = host.split('.')[-1]
    if ping_ip(host):
        try:
            ssh.connect(hostname=host,port=int(port),username=username,password=password)
            # 获取命令结果
            # command_mac = "/usr/sbin/ifconfig | grep ether | awk 'NR==1 {print $2}'"
            # stdin,stdout,stderr = ssh.exec_command(command_mac)
            # status = stdout.read().decode('UTF-8').strip()
            # record_host_status(host_mark,status)
            # print(host,'<-->','[',status,']')
            
            #command_date = f'ls -l /etc/supervisor/conf.d/'
            #stdin,stdout,stderr = ssh.exec_command(command_date)
            #status = stdout.read().decode('UTF-8').strip()
            # record_host_status(host_mark,status)
            #print(host,'<-->','[',status,']')

            # 执行reboot命令
            command_reboot = f'/sbin/reboot'
            ssh.exec_command(command_reboot)
        except:
            print(f"\033[1;31m * {host} cannot be connected !!!\033[0m")
#            print(f' * {host} cannot be connected !!!')
            time.sleep(0.2)
        finally:
            ssh.close()

    else:
        print(f"\033[1;31m {host} cannot be connected !!!\033[0m")
#        print(f'{host} cannot be connect !!!') 


def split_host_info(host_info):
    host,port,username,password = host_info.split(';')
    return host,port,username,password


def get_host_info():
    file = 'host.conf'   # 配置文件
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]

    return host_info

def main(WORD_THREAD):
    threads = []
    for i in range(WORD_THREAD):
        thread = threading.Thread(target=send_command)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


def call():
    host_info = get_host_info()
    WORD_THREAD = len(host_info)
    [IP_QUEUE.put(i) for i in host_info]
    try:
        main(WORD_THREAD)
    except:
        print("Error...")


if __name__ == '__main__':
    call()

