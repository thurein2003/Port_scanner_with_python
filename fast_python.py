# This is port scaning tools by Thu Rein Oo
# Date  22/Sep/2023

import argparse
import socket
from colorama import init, Fore

from threading import  Thread, Lock
from queue import Queue

#some colors
init ()
Green = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX

#NUMBER OF THREADS, FEEL free to tune this parameter as you wish
N_THREADS = 200
#THred queue
q = Queue()
print_lock = Lock()

def port_scan(port):
    #scan a port golbal variable host
    try:
        s = socket.socket()
        s.connect((host,port))
    except:
        with print_lock:
            print(f"{GRAY}{host:15}:{port:5} is closed {RESET}", end='\r')
    else:
        with print_lock:
            print(f"{Green}{host:15}:{port:5} is open {RESET}")
    finally:
        s.close()

def scan_thread():
    global q
    while True:
        #to get port numbers
        worker = q.get()
        port_scan(worker)
        q.task_done()

def main(host, ports):
    global q
    for t in range(N_THREADS):
        #for each
        t = Thread(target=scan_thread)
        t.daemon = True
        t.start()

    for worker in ports:
        q.put(worker)
        q.join()

if __name__ == "__main__" :
    parser = argparse.ArgumentParser(description="Simple ports scanner")
    parser.add_argument("host", help = "host to scan")
    parser.add_argument("--ports", dest="port_range", default="1-65535", help = "port range to scan, default is 1-65535(all port)")
    args = parser.parse_args()
    host, port_range = args.host, args.port_range

    start_port, end_port = port_range.split("-")
    start_port, end_port = int(start_port), int(end_port)

    ports = [p for p in range(start_port, end_port)]

    main(host, ports)