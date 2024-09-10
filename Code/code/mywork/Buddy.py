import pandas as pd
import numpy as np
import json
import glob
from Buddyconfig import config,Task,ALLTasks,Node,Groups,getNodeStatus
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
nodes=[Node(cardsPerNode) for _ in range(nodeNum)]
getNodeStatus(nodes)
groups=Groups(cardsPerNode,nodes)
getNodeStatus(nodes)
'''这里的队列可以考虑制作一个优先队列，对不同的任务进行优先级的评估'''
wl=[]

for currentTime in range(startTime,endTime,10):
    while sortedTasks[0].createTime <= currentTime:
        task=sortedTasks[0]
        sortedTasks.remove(0)
        wl.append(task)

    #依次处理wl里面的每一个task
    for task in wl:
        group = groups[task.cards]      #拿到一个合适的组，查找组里的资源
        if group is None:   #找不到合适的组那么就直接跳过
            continue
        else:




    # G.popTask(currentTime)
    # if len(sortedTasks) == 0:
    #     if nodes.isEmpty():
    #         break
    #     continue
    # else:
    #     while sortedTasks[0].createTime <= currentTime:
    #         status=nodes.putTask(sortedTasks[0],currentTime)
    #         if status is False:
    #             break
    #         del sortedTasks[0]
    #         count+=1
    #         print(f'{count}/{tasksNum}')
    #         if len(sortedTasks) == 0:
    #             break;
    #         # if count==6:
    #         #     input()
    # info=nodes.cal()
    # # print(f'{count}/{tasksNum}',end=' ')
    # # print(info)
    # time.append(currentTime)
    # piecesRate.append(info['piecesRate'])
    # nodeOccupiedRate.append(info['nodeOccupiedRate'])
    # act.append(info['act'])
    # emptycards.append(info['emptycards'])




