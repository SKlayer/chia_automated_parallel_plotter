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
parser.add_argument("-d1", "--delay1", type=str, required=True, help="Delay of the first phase")
parser.add_argument("-d2", "--delay2", type=str, required=True, help="To start new plotting")
parser.add_argument("-d", "--distance", type=str, required=False, help="Time between each plot starts")
parser.add_argument("-a", "--amount", type=str, required=True, help="Amount of plots Parallel")
parser.add_argument("-r", "--cores", type=str, required=False, help="Cores per plot (default: 2)")
parser.add_argument("-b", "--ram", type=str, required=False, help="Ram per Plot (default: 3390)")
parser.add_argument("-n", "--queued", type=str, required=False, help="Queued Plots (default: 1)")
parser.add_argument("-k", "--plot", type=str, required=False, help="Plot (default: 32)")
parser.add_argument("-t", "--temporary", type=str, required=True, help="Temporary Devices")
parser.add_argument("-f", "--target", type=str, required=True, help="Target Device")
parser.add_argument("-m", "--remote", type=bool, required=False, help="Remote Machine")
parser.add_argument("-fk", "--farmerkey", type=str, required=False, help="Farmer Key")
parser.add_argument("-pk", "--poolkey", type=str, required=False, help="Pool Key")

start = datetime.timestamp(datetime.now())
threads = []
args = parser.parse_args()
distance = 900 if not args.distance else int(args.distance)

def create_chia_threads():
    try:
        thread_list = []      

        plot_size = 32 if not args.plot else args.plot
        ram_size = 3390 if not args.ram else args.ram
        queue_size = 1 if not args.queued else args.queued
        cores = 2 if not args.cores else args.cores
        temp = args.temporary.split(";")
        target = args.target.split(";")
        
        for i in range(0,int(args.amount)):
            command = 'chia plots create' \
                            + ' -k ' + str(plot_size) \
                            + ' -n ' + str(queue_size) \
                            + ' -b ' + str(ram_size) \
                            + ' -r ' + str(cores) \
                            + ' -t ' + temp[i % len(temp)] \
                            + ' -d ' + target[i % len(target)] if not args.remote else  'chia plots create' \
                            + ' -f ' + args.farmerkey \
                            + ' -p ' + args.poolkey \
                            + ' -k ' + str(plot_size) \
                            + ' -n ' + str(queue_size) \
                            + ' -b ' + str(ram_size) \
                            + ' -r ' + str(cores) \
                            + ' -t ' + temp[i % len(temp)] \
                            + ' -d ' + target[i % len(target)] 
            thread = threading.Thread(target=os.system, args=(command,))
            thread_list.append(thread)
            logger.stdout_logger.debug('[CAPP] ['+str(datetime.now()) + ']' +' Plot ' + str(i) + ' created.')
        return thread_list
    except:
        logger.stdout_logger.error('[CAPP] ['+str(datetime.now()) + ']' +' Failed.')
        print(traceback.format_exc())

def schedule_chia_threads():

    thread_list = create_chia_threads()
    
    if len(threads) > 1:
        for ind, thread in enumerate(threads[0]):
            thread.join()
            while thread.isAlive():
                time.sleep(5)
            if not thread.isAlive():
                if ind == 0:
                    start = datetime.timestamp(datetime.now())
                thread_list[ind].start()
                time.sleep(distance)
        threads.pop(0)
        threads.append(thread_list)
    else:
        start = datetime.timestamp(datetime.now())
        for thread in thread_list:
            thread.start()
            time.sleep(distance)
        threads.append(thread_list)

def start_chia_automate_routine():  
    count = 0
    while True:
        
        while True:
            count += 1
            schedule_chia_threads()
            
            if count == len(args.temporary.split(";")):
                break

            time.sleep(int(args.delay1) - (len(threads[0]) * distance))

        time.sleep(int(args.delay2) - (datetime.timestamp(datetime.now()) - start))
        count = 0

if __name__ == '__main__':
    start_chia_automate_routine()
