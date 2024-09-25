import dataPrepare
import config
import time
from algorithms import FCFS, Buddy, SJF, BF, WF, NF
from log import logger
import tool
import analysis

'''
FCFS: First Come First Sever, 先到先服务算法
Buddy:我的算法
SJF:Short Job First, 短作业优先算法
BF: Best Fit, 最优适应算法
WF: Worst Fit, 最差适应算法
NF: Next Fit, 循环适应算法 
'''
# algorithms = [FCFS, Buddy, SJF, BF, WF, NF]
algorithms = [FCFS,Buddy]
tasks = dataPrepare.read_and_createTasks(config.file_path)
# analysis.plot_histograms(tasks)
for algorithm in algorithms:
    '''
    algorithm return:
        每个step统计的任务平均完成时间(act)
        每个step统计的空闲卡的数量
        每个step中，统计调度前后，wl中任务卡数的变化
        每个step统计的任务的平均等待时间
    '''
    logger.log(str(algorithm) + 'is start!')
    algorithm().run(tasks)


for algorithm in algorithms:
    tool.plot_data(algorithm().algorithm_name)


