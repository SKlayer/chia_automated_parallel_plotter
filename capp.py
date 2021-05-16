import argparse
import os
from datetime import datetime
import traceback
import time
from logger import LoggerFactory
from subprocess import Popen
import threading
from concurrent.futures import ThreadPoolExecutor

logger = LoggerFactory()

parser = argparse.ArgumentParser(description="This module will create chia plots as defined via params")
parser.add_argument("-d1", "--delay1", type=str, required=False, help="Delay of the first phase")
parser.add_argument("-d2", "--delay2", type=str, required=False, help="To start new plotting")
parser.add_argument("-c", "--copytime", type=str, required=False, help="Time to copy files from temporary to destination")
parser.add_argument("-d", "--distance", type=str, required=False, help="Time between each plot starts")
parser.add_argument("-a", "--amount", type=str, required=False, help="Amount of plots Parallel")
parser.add_argument("-r", "--cores", type=str, required=False, help="Cores per plot")
parser.add_argument("-b", "--ram", type=str, required=False, help="Ram per Plot")
parser.add_argument("-n", "--queued", type=str, required=False, help="Queued Plots")
parser.add_argument("-k", "--plot", type=str, required=False, help="Plot (default: 32)")
parser.add_argument("-t", "--temporary", type=str, required=False, help="Temporary Devices")
parser.add_argument("-f", "--target", type=str, required=False, help="Target Device ")

args = parser.parse_args()

def create_chia_threads():
    try:
        plot_size = 32
        ram_size = 3390
        queue_size = 1
        cores = 2

        thread_list = []

        if args.plot:
            plot_size = args.plot
        if args.ram:
            ram_size = args.ram
        if args.queued:
            queue_size = args.queued
        if args.cores:
            cores = args.cores

        temp = args.temporary.split(";")
        tar = args.target.split(";")
        
        for i in range(0,int(args.amount)):
            command = 'chia plots create' \
                        + ' -k ' + plot_size \
                        + ' -n ' + queue_size \
                        + ' -b ' + ram_size \
                        + ' -r ' + cores \
                        + ' -t ' + temp[i % len(temp)] +":\\" \
                        + ' -d ' + tar[i % len(tar)] +":\\"
            thread = threading.Thread(target=os.system, args=(command,))
            thread_list.append(thread)
            logger.stdout_logger.debug('[CAPP] ['+str(datetime.now()) + ']' +' Plot ' + str(i) + ' created.')
        return thread_list
    except:
        logger.stdout_logger.error('[CAPP] ['+str(datetime.now()) + ']' +' Failed.')
        print(traceback.format_exc())

def start_chia_threads(distance):
    thread_list = create_chia_threads()
    for thread in thread_list:
        thread.start()
        time.sleep(distance)
    return thread_list

def check_aliveness(threads):
    for thread in threads:
        while thread.isAlive():
            time.sleep(120)
        thread.join()

def start_chia_automate_modus():
    start = datetime.timestamp(datetime.now())
    threads = []
    count = 0
    distance = 900

    if args.distance:
        distance = int(args.distance)
        
    while True:
        while True:
            count += 1
            threads.append(start_chia_threads(distance))
            
            if count == len(args.temporary.split(";")):
                break

            time.sleep(int(args.delay1) - (len(threads[0]) * distance))

            if count == 1 and len(threads) > 1:
                check_aliveness(threads[0])
                threads.pop(0)

        time.sleep(int(args.delay2) - (datetime.timestamp(datetime.now()) - start))

        check_aliveness(threads[0])
        threads.pop(0)

        start = datetime.timestamp(datetime.now())
        count = 0

if __name__ == '__main__':
    start_chia_automate_modus()
