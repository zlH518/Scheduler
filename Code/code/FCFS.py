import pandas as pd
import numpy as np
import os
import json
import glob
from config import config,Task,ALLTasks
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
allData=ALLTasks(['startTime','schedulingTime','createTime','duration','cards'],data)
print(len(data))

# cards_counts = np.unique(allData.matrix[:, 4], return_counts=True)
#
# plt.figure(figsize=(8, 8))
# plt.pie(cards_counts[1], labels=cards_counts[0], autopct='%1.1f%%', startangle=90)
# plt.axis('equal')
# plt.title('Distribution of Cards')
# plt.show()


sortedTasks = sorted(allData.allTask, key=lambda x: x.createTime)

nodeStatus = {i: {'available_cards': cardsPerNode, 'next_task_start': 0} for i in range(nodeNum)}

schedule_result = []

# 遍历排序后的任务列表
for task in sorted_tasks:
    # 找到第一个可用的节点
    for node_id, status in node_status.items():
        if status['available_cards'] >= task.cards and (status['next_task_start'] == 0 or task.startTime >= status['next_task_start']):
            # 更新节点状态
            node_status[node_id]['available_cards'] -= task.cards
            node_status[node_id]['next_task_start'] = task.startTime + task.durationTime
            # 记录调度结果
            schedule_result.append((node_id, task))
            break

# 打印调度结果
for result in schedule_result:
    node_id, task = result
    print(f"Node {node_id} scheduled Task with create time {task.createTime}, start time {task.startTime}, duration {task.durationTime}, cards {task.cards}")