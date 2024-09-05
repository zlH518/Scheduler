import pandas as pd
import numpy as np
import os
import json
import glob
from config import config,Task,ALLTasks,Node
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
assert len(data) == len(ALLTasks)

Gnum = config['GNum']
G = [[Node(cardsPerNode) for _ in range(nodeNum/5)] for _ in range(Gnum)]




