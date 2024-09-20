import pandas as pd
import numpy as np
import os
import json
import glob
from FCFSconfig import config,Task,ALLTasks,Nodes
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import re
# from torch.utils.tensorboard import SummaryWriter
#
# writer = SummaryWriter('C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\log')


def convert_timestamp_to_seconds(date_str):
    # 解析日期字符串，注意加上时区信息
    date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S%z')
    # 转换为自1970年1月1日以来的秒数
    timestamp = date_obj.timestamp()
def read_csv_and_create_tasks(csv_file_path):
    task_list = []
    with open(csv_file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            # 检查gpu_num是否大于0且小于或等于8
            gpu_num = int(row['gpu_num'])
            if 0 < gpu_num <= 8:
                task = Task(
                    startTime=convert_timestamp_to_seconds(row['start_time']),
                    schedulingTime=convert_timestamp_to_seconds(row['end_time'])-convert_timestamp_to_seconds(row['submit_time']),
                    createTime=convert_timestamp_to_seconds(row['submit_time']),
                    duration=int(row['duration']),
                    cards=gpu_num
                )
                task_list.append(task)
    return task_list

def FCFS():
    csv_path="C:\\Users\\Administrator\\Desktop\\IdsLab\\任务\\SchedulerSystem\\Code\\data\\newData\\trace_seren.csv"
    # nodeNum=config['nodeNum']
    # cardsPerNode=config['cardsPerNode']
    # dataPath=config['dataPath']
    # paths=glob.glob(dataPath)
    # dfs=[]      #only complete,分pool
    # sum=0
    # for i,path in enumerate(paths):
    #     with open(path,'r') as f:
    #         json_data = json.load(f)
    #         dft = pd.DataFrame(json_data)
    #         dft.reset_index(inplace=True)
    #         dft=dft[dft['status.phase']=='Completed']
    #         dft=dft[dft['spec.resource.node_count']==1]
    #         sum+=len(dft)
    #         dft = dft.drop('index',axis=1)
    #         dfs.append(dft)
    #
    # df1,df2,df3,df4,df5,df6 = dfs
    # dataframes = [df1,df2,df3,df4,df5,df6]
    #
    # #df1:218,126;   df2:16,104; df3:5798,378;   df4:203,144     df5:1627,230    df6:484,254
    # for i,df in enumerate(dataframes):
    #     mask = df['status.start_time'].isna() | df['metadata.create_time'].isna() | (df['status.start_time']== None) | (df['metadata.create_time']== None) | (df['status.start_time']==0) | (df['metadata.create_time']==0)
    #     df['scheduling_time'] = (np.where(mask,np.nan, df['status.start_time']-df['metadata.create_time']))/1000
    #     df['metadata.create_time']=(df['metadata.create_time']-df['metadata.create_time'].min())/1000
    #     df['status.start_time'] = (df['status.start_time'] - df['status.start_time'].min())/1000
    #     df['status.duration'] = df['status.duration'] / 1000
    #     df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.8xlarge', 8)
    #     df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.4xlarge', 4)
    #     df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.2xlarge', 2)
    #     df['spec.resource.flavor_id'] = df['spec.resource.flavor_id'].replace('modelarts.pool.visual.xlarge', 1)
    #     df = df.dropna(subset=['scheduling_time'])
    #     dfs[i] = [Task(row['status.start_time'],row['scheduling_time'],row['metadata.create_time'],row['status.duration'],row['spec.resource.flavor_id']) for index, row in df.iterrows()]
    #
    # data=[]
    # for df in dfs:
    #     for d in df:
    #         data.append(d)
    data=read_csv_and_create_tasks(csv_file_path=csv_path)
    allData=ALLTasks(['startTime','schedulingTime','createTime','duration','cards','endTime'],data)
    print(len(data))

    # cards_counts = np.unique(allData.matrix[:, 4], return_counts=True)
    #
    # plt.figure(figsize=(8, 8))
    # plt.pie(cards_counts[1], labels=cards_counts[0], autopct='%1.1f%%', startangle=90)
    # plt.axis('equal')
    # plt.title('Distribution of Cards')
    # plt.show()


    sortedTasks = sorted(allData.allTask, key=lambda x: x.createTime)
    nodes=Nodes(nodesNum=config['nodeNum'], cardsPerNode=config['cardsPerNode'])
    startTime=int(sortedTasks[0].createTime)
    endTime=int(max(allData.matrix[0]+allData.matrix[1]))
    tasksNum=len(sortedTasks)
    count=0
    piecesRate=[]
    nodeOccupiedRate=[]
    act=[]
    emptycards=[]
    time=[]
    for currentTime in range(startTime,endTime,10):
        nodes.popTask(currentTime)
        if len(sortedTasks) == 0:
            if nodes.isEmpty():
                break
            continue
        else:
            while sortedTasks[0].createTime <= currentTime:
                status=nodes.putTask(sortedTasks[0],currentTime)
                if status is False:
                    break
                del sortedTasks[0]
                count+=1
                print(f'{count}/{tasksNum}')
                if len(sortedTasks) == 0:
                    break;
                # if count==6:
                #     input()
        info=nodes.cal()
        # print(f'{count}/{tasksNum}',end=' ')
        # print(info)
        time.append(currentTime)
        piecesRate.append(info['piecesRate'])
        nodeOccupiedRate.append(info['nodeOccupiedRate'])
        act.append(info['act'])
        emptycards.append(info['emptycards'])
    #     writer.add_scalar('piecesRate',info['piecesRate'], currentTime)
    #     writer.add_scalar('nodeOccupiedRate', info['nodeOccupiedRate'], currentTime)
    #     writer.add_scalar('act', info['act'], currentTime)
    #     writer.add_scalar('emptycards', info['emptycards'], currentTime)
    # writer.close()

    # fig, axs = plt.subplots(2, 2, figsize=(14, 10))
    #
    # axs[0, 0].plot(time, piecesRate, label='piecesRate')
    # axs[0, 0].set_title('PiecesRate')
    # axs[0, 0].set_xlabel('Time')
    # axs[0, 0].set_ylabel('Rate')
    # axs[0, 0].legend()
    #
    # axs[0, 1].plot(time, nodeOccupiedRate, label='nodeOccupiedRate', color='orange')
    # axs[0, 1].set_title('Node Occupied Rate')
    # axs[0, 1].set_xlabel('Time')
    # axs[0, 1].set_ylabel('Rate')
    # axs[0, 1].legend()
    #
    plt.plot(time, act, label='act', color='green')
    plt.title('ACT')  # 设置图表标题
    plt.xlabel('Time')  # 设置X轴标签
    plt.ylabel('ACT')  # 设置Y轴标签
    plt.legend()  # 显示图例
    #
    # axs[1, 1].plot(time, emptycards, label='emptycards', color='red')
    # axs[1, 1].set_title('Empty Cards')
    # axs[1, 1].set_xlabel('Time')
    # axs[1, 1].set_ylabel('Count')
    # axs[1, 1].legend()
    # plt.tight_layout()
    plt.savefig('C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\FCFSNewData.png')
    plt.show()
    return time,act

FCFS()