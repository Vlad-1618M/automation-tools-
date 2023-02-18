#!/usr/bin/env python
from ast import For
from asyncore import file_dispatcher
from posixpath import splitext
import readline
import time
import psutil
import datetime
import argparse
from colorama import Fore, Style

def get_running_processes_by_name(name):
    matching_processes = psutil.process_iter(attrs=['name', 'create_time', 'pid'])
    processes_by_name = {}

    for process in matching_processes:
        if name.lower() in process.info['name'].lower():
            pid = process.info['pid']
            ps_name = process.info['name']
            ps_runtime = process.info['create_time']
            if ps_name not in processes_by_name:
                processes_by_name[ps_name] = []
            processes_by_name[ps_name].append((ps_name, pid, ps_runtime))

    result = []
    for name, processes in processes_by_name.items():
        if len(processes) == 1:
            result.append(processes[0])
        else:
            pids = set([ps[1] for ps in processes])
            for pid in pids:
                runtime = min([ps[2] for ps in processes if ps[1] == pid])
                runtime_str = datetime.datetime.fromtimestamp(runtime).strftime('%Y-%m-%d %H:%M:%S')
                result.append((name, str(pid), runtime_str))

    return result


def measure_cpu_usage(name):
    processes = get_running_processes_by_name(name)
    if not processes:
        return None
    pid = processes[0][1]
    process = psutil.Process(pid)
    cpu_percent = process.cpu_percent(interval=1)
    return cpu_percent


def measure_memory_usage(name):
    processes = get_running_processes_by_name(name)
    if not processes:
        return None
    pid = processes[0][1]
    process = psutil.Process(pid)
    memory_info = process.memory_info()
    # return memory_info.rss / 1e9
    return memory_info.rss


def measure_disk_usage():
    disk_usage = psutil.disk_usage("/")
    return disk_usage.percent


def output_to_file(name, cpu_usage, memory_usage, disk_usage, file, count):
    processes = get_running_processes_by_name(name)
    if not processes:
        return
    
    file.write(f"Date & Time:\t{time.ctime()}\t"
               f"PS_Name: {processes[0][0]}\tPS_ID: {processes[0][1]}\tCPU Usage: {cpu_usage} %"
               f"\tRAM Usage:\tin MB {memory_usage / (1024 ** 2)}\t in GB {memory_usage / (1024 ** 3)}"
               f"\t Disk Usage: {disk_usage} %\t \tCount: {count}\n")


def output_to_terminal(name, cpu_usage, memory_usage, disk_usage, count):
    processes = get_running_processes_by_name(name)
    if not processes:
        return
        
    print(f"{Fore.RESET}Date & Time:\t{Fore.YELLOW + Style.BRIGHT}{time.ctime()}"
         f"\t{Fore.RESET}Process Name: {Fore.GREEN}{processes[0][0]}"
         f"\t{Fore.RESET}Process ID: {Fore.GREEN}{processes[0][1]}"
         f"\t{Fore.RESET}OS {Fore.LIGHTCYAN_EX}CPU Usage: {Fore.YELLOW}{cpu_usage} {Fore.MAGENTA}%"
         f" {Fore.RESET}\tOS {Fore.LIGHTCYAN_EX}Memory Usage: {Fore.MAGENTA}   in MB {Fore.YELLOW}{memory_usage / (1024 ** 2)} {Fore.MAGENTA}  in GB {Fore.YELLOW}{memory_usage / (1024 ** 3)}"
         f"\t{Fore.RESET}OS {Fore.LIGHTCYAN_EX}Disk Usage: {Fore.YELLOW}{disk_usage} {Fore.MAGENTA}%\t{Fore.RESET}Count:{Fore.LIGHTRED_EX} {count}")


def main(ps_name):
    loop_count = 0
    while True: 
        loop_count += 1
        cpu_usage = measure_cpu_usage(name=ps_name)
        memory_usage = measure_memory_usage(name=ps_name)
        disk_usage = measure_disk_usage()
        if output_type == "file":
            with open(f"monitor_process_{args.process_name}.txt", "a") as file:
                output_to_file(ps_name, cpu_usage, memory_usage, disk_usage, file, count=loop_count)
                if loop_count >= 100:
                    print(f'\n{Fore.YELLOW}{Style.BRIGHT}The file write has reached its limit of {Fore.RED}{loop_count} {Fore.YELLOW}lines\nReading file now ...')
                    with open(f"monitor_process_{args.process_name}.txt", "r") as file:
                        for read_from in file.readlines():
                            time.sleep(0.04)
                            # print(cleanup.splitlines()[0], flush=True)
                            print(read_from.replace('\t', '').splitlines()[0], flush=True)
                        break
        else:
            output_to_terminal(ps_name, cpu_usage, memory_usage, disk_usage, count=loop_count)
        time.sleep(0.004)


def convert_to_gb(memory_size):
    if memory_size < 0:
        raise ValueError("Memory size must be a positive number.")
    
    divisor = pow(1024, 2) if memory_size < pow(1024, 2) else pow(1024, 3)
    return round(memory_size / divisor, 2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Measure CPU, memory, and disk usage of a process')
    parser.add_argument('process_name', type=str, help='Name of the process to monitor')
    parser.add_argument("-o", "--output", choices=["file", "terminal"], default="terminal", help="The output type (file or terminal). Default is terminal.")
    args = parser.parse_args()
    output_type = args.output
    main(args.process_name)
    
