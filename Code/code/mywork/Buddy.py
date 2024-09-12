import pandas as pd
import numpy as np
import json
import glob
from Buddyconfig import config,Task,ALLTasks,Node,Groups,getNodeStatus,nodes
import matplotlib.pyplot as plt



nodeNum=config['nodeNum']
cardsPerNode=config['cardsPerNode']
dataPath=config['dataPath']
paths=glob.glob(dataPath)
dfs=[]      #only complete,分pool
sum=0
for i,path in enumerate(paths):
    with open(path,'r') as f:
        json_data = json.load(f)
        dft = pd.DataFrame(json_data)
        dft.reset_index(inplace=True)
        dft=dft[dft['status.phase']=='Completed']
        dft=dft[dft['spec.resource.node_count']==1]
        sum+=len(dft)
        dft = dft.drop('index',axis=1)
        dfs.append(dft)

df1,df2,df3,df4,df5,df6 = dfs
dataframes = [df1,df2,df3,df4,df5,df6]

#df1:218,126;   df2:16,104; df3:5798,378;   df4:203,144     df5:1627,230    df6:484,254
for i,df in enumerate(dataframes):
    mask = df['status.start_time'].isna() | df['metadata.create_time'].isna() | (df['status.start_time']== None) | (df['metadata.create_time']== None) | (df['status.start_time']==0) | (df['metadata.create_time']==0)
    df['scheduling_time'] = (np.where(mask,np.nan, df['status.start_time']-df['metadata.create_time']))/1000
    df['metadata.create_time']=(df['metadata.create_time']-df['metadata.create_time'].min())/1000
    df['status.start_time'] = (df['status.start_time'] - df['status.start_time'].min())/1000
    df['status.duration'] = df['status.duration'] / 1000
    df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.8xlarge', 8)
    df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.4xlarge', 4)
    df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.2xlarge', 2)
    df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.xlarge', 1)
    df = df.dropna(subset=['scheduling_time'])
    dfs[i] = [Task(row['status.start_time'],row['scheduling_time'],row['metadata.create_time'],row['status.duration'],row['spec.resource.flavor_id']) for index, row in df.iterrows()]

data=[]
for df in dfs:
    for d in df:
        data.append(d)
allData=ALLTasks(['startTime','schedulingTime','createTime','duration','cards','endTime'],data)
assert len(data) == len(allData)

sortedTasks = sorted(allData.allTask, key=lambda x: x.createTime)
startTime=int(sortedTasks[0].createTime)
endTime=int(max(allData.matrix[0]+allData.matrix[1]))
getNodeStatus(nodes)
groups=Groups(cardsPerNode,nodes)
getNodeStatus(nodes)
'''这里的队列可以考虑制作一个优先队列，对不同的任务进行优先级的评估,
    目前对优先级的评估包括小任务，以及对当前节点状态的适配度，
    或者可不可以用强化学习来做
'''
wl=[]

for currentTime in range(startTime,endTime,10):
    #首先查看是否有需要释放的任务
    groups.popTask(currentTime)

    #查看是否到了需要调度的时刻，需要则对各个组中空闲的资源重新分配
    while sortedTasks[0].createTime <= currentTime:
        task=sortedTasks[0]
        del sortedTasks[0]
        wl.insert(0,task)

    #依次处理wl里面的每一个task
    for task in reversed(wl):
        group = groups[task.cards]      #拿到一个合适的组，查找组里的资源
        if group is None:   #找不到合适的组那么说明没有资源可以处理这个任务，则继续放在wl里面
            continue
        else:               #如果找到合适的组了就放置任务，同时从wl中去除
            group.putTask(task,currentTime)
            wl.remove(task)

