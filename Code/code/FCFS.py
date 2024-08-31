import pandas as pd
import numpy as np
import os
import json
import glob
from config import config,Task

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
    dfs[i] = [Task(row['status.start_time'],row['schedulingTime,createTime,duration,cards']) for index, row in df.iterrows()]
print(1)












# DATAPATH="C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data\*.json"
# data=glob.glob(DATAPATH)
# titles=glob.glob(DATAPATH)
#
#
# dfs=[]      #only complete
# sum=0
# for title in titles:
#     if title.endswith('.json'):
#         with open(title,'r') as f:
#             json_data = json.load(f)
#             dft = pd.DataFrame(json_data)
#             dft.reset_index(inplace=True)
#             dft=dft[dft['status.phase']=='Completed']
#             sum+=len(dft)
#             dft = dft.drop('index',axis=1)
#             dfs.append(dft)
#
#
# df1,df2,df3,df4,df5,df6 = dfs
# dataframes = [df1,df2,df3,df4,df5,df6]
# for df in dataframes:
#     mask = df['status.start_time'].isna() | df['metadata.create_time'].isna() | (df['status.start_time']== None) | (df['metadata.create_time']== None) | (df['status.start_time']==0) | (df['metadata.create_time']==0)
#     df['scheduling_time'] = np.where(mask,np.nan, df['status.start_time']-df['metadata.create_time'])
#
# for df in dataframes:
#     df = df.dropna(subset=['scheduling_time'])
# pd.to_datetime('1708606592849', unit='ms')