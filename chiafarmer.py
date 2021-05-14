import argparse
import os
from datetime import datetime
import traceback
import time
from logger import LoggerFactory
from subprocess import Popen
import threading

logger = LoggerFactory()

parser = argparse.ArgumentParser(description="This module will create chia plots as defined via params")
parser.add_argument("-d1", "--delay1", type=str, required=False, help="Delay of the first phase")
parser.add_argument("-d2", "--delay2", type=str, required=False, help="To start new plotting")
parser.add_argument("-a", "--amount", type=str, required=False, help="Amount of plots Parallel")
parser.add_argument("-r", "--cores", type=str, required=False, help="Cores per plot")
parser.add_argument("-b", "--ram", type=str, required=False, help="Ram per Plot")
parser.add_argument("-n", "--queued", type=str, required=False, help="Queued Plots")
parser.add_argument("-k", "--plot", type=str, required=False, help="Plot (default: 32)")
parser.add_argument("-t", "--temporary", type=str, required=False, help="Temporary Devices")
parser.add_argument("-f", "--target", type=str, required=False, help="Target Device ")


def farm_chia():
    thread_list = []
    try:
        args = parser.parse_args()
        plot_size = 32
        if args.plot:
            plot_size = args.plot
        temp = args.temporary.split(";")
        tar = args.target.split(";")

        for i in range(0,int(args.amount)):
            command = 'chia plots create' \
                      + ' -k ' + plot_size \
                      + ' -n ' + args.queued \
                      + ' -b ' + args.ram \
                      + ' -r ' + args.cores \
                      + ' -t ' + temp[i % len(temp)] \
                      + ' -d ' + tar[i % len(tar)]
            command = 'chia plots create' \
                      + ' -k ' + plot_size \
                      + ' -n ' + args.queued \
                      + ' -b ' + args.ram \
                      + ' -r ' + args.cores \
                      + ' -t ' + temp[i % len(temp)] +":\\" \
                      + ' -d ' + tar[i % len(tar)] +":\\"
            thread = threading.Thread(target=os.system, args=(command,))
            thread_list.append(thread)
            logger.stdout_logger.debug('[Chia Farmer] ['+str(datetime.now()) + ']' +' Plot ' + str(i) + ' created.')
        return thread_list
    except:
        logger.stdout_logger.error('[Chia Farmer] ['+str(datetime.now()) + ']' +' Failed.')
        print(traceback.format_exc())

if __name__ == '__main__':
    args = parser.parse_args()
    start = datetime.timestamp(datetime.now())
    threads = []
    count = 0
    while True:
        while True:
            count += 1
            thread_list = farm_chia()
            threads.append(thread_list)
            for thread in thread_list:
                thread.start()

            if count == 2:
                break

            time.sleep(int(args.delay1))

            if count == 1 and len(threads) > 1:
                for thread in threads[0]:
                    thread.join()

        time.sleep(int(args.delay2) - (datetime.timestamp(datetime.now()) - start))
        for thread in threads[0]:
            thread.join()
        threads.pop(0)
        start = datetime.timestamp(datetime.now())
        count = 0
