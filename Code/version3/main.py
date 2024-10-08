import dataPrepare
import config
import time
from FCFS import FCFS
from task import Task
from node import Node
from log import logger
import tool

'''
FCFS: First Come First Sever, 先到先服务算法,先拿单纯的FCFS和增加了迁移的相比较
Buddy:我的算法
SJF:Short Job First, 短作业优先算法,这里任务太多，如果等待所有任务到来再做短任务优先的话非常不合适，因此打算阶段性短作业优先
BF: Best Fit, 最优适应算法
WF: Worst Fit, 最差适应算法
NF: Next Fit, 循环适应算法 

'''
# algorithms = [FCFS, Buddy, SJF, BF, WF, NF]
algorithms = [FCFS]
for algorithm in algorithms:
    Task.reset()                            #创建任务
    Node.reset()                            #创建节点
    algorithm()                             #算法初始化
    algorithm().run()                       #算法运行
    algorithm().recoder()                   #算法记录结果
    print(len(Task.Tasks))



