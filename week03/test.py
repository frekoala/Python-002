import argparse
import ping3 
import re
from IPy import IP
from concurrent.futures import ThreadPoolExecutor
# from queue import Queue
import time
import json
# import threading
from multiprocessing.dummy import Pool as ThreadPool
import socket
import struct

def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False

def ping(ip_list, file = None):
        try:
            for ip in ip_list:
                delay = ping3.ping(ip,timeout = 1)
                result_dict = {}
                if delay:
                    print(f'{ip}可以ping通,延时:{delay}s')
                    result_dict['result'] = f'{ip}可以ping通,延时:{delay}s'
                else:
                    print(f'{ip} ping不通！！！')
                    result_dict['result'] = f'{ip} ping不通！！！'
                if file:
                    json.dump(result_dict,fp=file,ensure_ascii=False) 
        except Exception as e:
            print(e)


def get_ping_list(ip):
    if ip.find('-') == 0:
        ping_host(ip)
    ip_begin = ip.split('-')[0]
    ip_end = ip.split('-')[1]
    assert isIP(ip_begin), f"请输入正确的起始ip"
    assert isIP(ip_end), f"请输入正确的结束ip"
    
    # 列出网段内所有ip
    ip_list = []
    for par4 in range(int(ip_begin.split('.')[3]) + 1, int(ip_end.split('.')[3]) + 1):
        ip_list.append(f"{ip_begin.split('.')[0]}.{ip_begin.split('.')[1]}.{ip_begin.split('.')[2]}.{par4}")
    print(ip_list)
    return ip_list


def findIPs(start, end):
    ipstruct = struct.Struct('>I')
    start, = ipstruct.unpack(socket.inet_aton(start))
    end, = ipstruct.unpack(socket.inet_aton(end))
    return [socket.inet_ntoa(ipstruct.pack(i)) for i in range(start, end + 1)]


def tcp(ip, file = None):
    assert isIP(ip), f"请输入正确的ip"
    sk=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    # 只取1~1024
    # for port in range(1,1025):
    for port in range(3305,3308):
        result = sk.connect_ex((ip,port))
        result_dict = {}
        if result == 0:
            print(f'{ip}:{port} is open')
            result_dict['result'] = f'{ip}:{port} is open'
        else:
            print(f'{ip}:{port} is close')
            result_dict['result'] = f'{ip}:{port} is close'
        if file:
            json.dump(result_dict,fp=file,ensure_ascii=False) 

def ping_or_tcp(func, ip_addr, num = 1,*args, **kwargs):
    # mult_tpye = kwargs.get("mult_tpye")
    # num = kwargs.get("num")
    file = kwargs.get("file")

    # 将结果保存到一个json文件中
    if file:
        output = open(file,'a',encoding='gbk') 
    else:
        output = ''

    # 默认使用多线程
    if func == 'ping':
        ip_list = get_ping_list(ip_addr)

        with ThreadPoolExecutor(num) as executor_ping:
            try:
                # executor.map(ping, ip_list)
                executor_ping.submit(ping,ip_list,output)
            except Exception as e:
                print(e)
    if func == 'tcp':
        with ThreadPoolExecutor(num) as executor_tcp:
            try:
                # executor.map(ping, ip_list)
                executor_tcp.submit(tcp,ip_addr,output)
            except Exception as e:
                print(e)
    if file:
        output.close()
   
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", dest='num', default=1, help="Concurrent quantity", type=int)
    parser.add_argument("-f", dest='func', choices=['ping', 'tcp'], help='Specify the required function, "ping" means ip address scanning, ''"tcp" means port scanning')
    parser.add_argument("-ip", dest='ip_addr', help="IP address or Continuous IP address")
    parser.add_argument("-w", dest='file', help="save the result in a file")
    # parser.add_argument("-m", dest='mult_tpye', choices=['proc', 'thread'], help='use the multiple process or multiple thread')
    args = parser.parse_args()
    # ping_or_telnet(num=args.num, func=args.func, ip_addr=args.ip_addr, file=args.file, mult_tpye=args.mult_tpye)
    start_time = time.time()
    ping_or_tcp(num=args.num, func=args.func, ip_addr=args.ip_addr, file=args.file)
    end_time = time.time()
    print(f'耗时:{end_time - end_time}s')

if __name__ == "__main__":
    main()
    # ping_or_tcp('ping','192.168.0.0-192.168.0.100',4,file='result.json')
    # ping_or_tcp('tcp','127.0.0.1',4,file='result.json')
    # telnet('127.0.0.1')
