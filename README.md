#Chai Automated Parallel Plotter - CAPP

This project was initiated by Chia Farming via CLI.

The python program should improve the handling with the CLI and automate the plotting process.

This program addresses four main problems which occured via plotting parallel via CLI

* Delays between plots
* Multiple temporary devices
* Multiple target devices
* Endless plotting process repected to resources

The use case was that I'd like to plot automated on a small server system with multiple SSDs and multiple HDDs. I've started
to determine the times of the different plotting phases. It is needed find the time of phase 1 and the time of the whole
plotting process. Based on these times it is possible to set up an automated endless plotting process with optimal output.

![Delay Times between Plots](delay_diagram.png "Delay between Plots")

The program starts first e.g. 6 plots parallel and after phase 1 of these plots is finished, it starts an other 6 parallel
plots. Each plot is executed in its own thread. After the first plots are finished the threads will be closed and an
other 6 plots were triggered and so on.

For this you can use the following params


|Parameter |Description |Example |
| --- | --- | --- |
|k |Plotsize |-k 32 (default: 32) |
|n |Amount of plots in queue |-n 1 (default: 1) |
|b |Amount of RAM in MB |-n 3390 (default: 3390) |
|r |Amount of Threads |-r 2 (default: 2) |
|t |Temporary devices separated with ; |-t A;B |
|f |Final target devices separated with ; |-f C |
|d1 |Delay 1 which corresponds with the Phase 1 time in seconds |-d1 12500 |
|d2 |Delay 2 which corresponds with Plotting time in seconds|-d2 32000 |
|a |Amount of parallel plots |-a 6 |

The program can be started via
```
    python chai_automated_parallel_plotter.py -k 32 -n 1 -b 3390 -r 2 -t Y;Z -f V -d1 12500 -d2 32000 -a 6
```
