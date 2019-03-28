import sys,os
import send_command
import time 
from queue import Queue
from configparser import ConfigParser
from itertools import chain
import platform
import subprocess
from threading import Thread

q1 = Queue()    # 设备登陆信息的队列
q2 = Queue()    # ping IP 的结果队列

def ping_ip():
    while not q1.empty():
        ip = q1.get().split(';')[0]
        if platform.system() == 'Windows':
            command = 'ping -n 2 -w 5 %s' % ip
        elif platform.system() == "Linux":
            command = 'ping -c 2 -w 5 %s' % ip
        res = subprocess.call(command,shell=True,stdout=subprocess.PIPE)
        info = ip + ' ' +str(1 if res == 0 else 0)
        # return [ip,True if res == 0 else False]
        q2.put(info)
        # return ip,True if res == 0 else False

def thread_ping():
    threads = []
    for i in range(5):
        thread = Thread(target=ping_ip)
        thread.start()
        threads.append(thread)

        # t = Thread(target=lambda q: q.put(ping_ip()), args=(q2,))
        # t.start()
        # threads.append(t)

    for thread in threads:
        thread.join()


def get_host_info():
    file = 'host.conf'   # 配置文件
    cfg = ConfigParser()
    with open(file,'r') as fp:
        cfg.read_file(chain(['[global]'], fp), source=file)
        hosts_list = cfg.get('test_hosts', 'hosts_nums').split(';')
        host_info = [cfg.get('test_hosts', i) for i in hosts_list]

    [q1.put(i) for i in host_info]

def record_host_status(host,info_times):
    """ 获取记录结果 写入文件中 """
    name = host.split('.')[-1]
    try:
        if not os.path.exists('run_result'):
            os.mkdir('run_result')
    except:
        pass
    with open(f'run_result/{name}_status.txt','a+') as s:
        tt = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        s.write(f'{tt} <--* {name} {info_times} *--> times\n')


def main(times,interval):
    for i in range(1,int(times)+1):
        print(f"-- test {i} --")
        get_host_info()     # 获取登陆信息
        thread_ping()		# ping 目标设备
        while not q2.empty(): 	# 获取ping 的结果
            host_mark,status = q2.get().split(' ')
            if int(status) == 1:

                info = f'{i} OK'
                record_host_status(host_mark, info)
            else:
                info = f"{i} ERROR"
                record_host_status(host_mark, info) 

        send_command.call()               # 执行命令

        time.sleep(int(interval))			# 等待一段时间 然后进行下次循环


if __name__ == '__main__':
	args = sys.argv
	if len(args) != 3:
#		print('Usage: python3 control.py (Testing_frequency) (Execution_interval)')
		print('Usage: \033[1;34;40mpython3 control.py (Testing_frequency) (Execution_interval)\033[0m')
	else:
		test_times, inerval= args[1:]
		with open("PID.txt",'w') as f:
			print(os.getpid(),file=f)	

		main(test_times,inerval)

