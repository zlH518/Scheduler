import dataPrepare
import config
import time
from algorithms import FCFS, Buddy, SJF, BF, WF, NF

'''
FCFS: First Come First Sever, 先到先服务算法
Buddy:我的算法
SJF:Short Job First, 短作业优先算法
BF: Best Fit, 最优适应算法
WF: Worst Fit, 最差适应算法
NF: Next Fit, 循环适应算法 
'''
algorithms = [FCFS, Buddy, SJF, BF, WF, NF]
tasks = dataPrepare.read_and_createTasks(config.file_path)
for algorithm in algorithms:
    '''
    algorithm return:
        每个step统计的任务平均完成时间(act)
        每个step统计的空闲卡的数量
        每个step中，统计调度前后，wl中任务卡数的变化
        每个step统计的任务的平均等待时间
    '''
    act, queuetime = algorithm(tasks)