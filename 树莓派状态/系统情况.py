import psutil
import os
import commands
import subprocess

psutil.cpu_count()
psutil.cpu_times()
psutil.virtual_memory()
psutil.swap_memory()
psutil.disk_partitions()
psutil.disk_usage("/")
psutil.disk_io_counters()
psutil.net_io_counters()
psutil.net_if_addrs()
psutil.net_if_stats()

os.popen('ls').readlines()

commands.getoutput('ls')

p = subprocess.Popen('ls',shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
p.stdout.readlines()