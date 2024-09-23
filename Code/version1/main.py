import dataPrepare
import config
import time
from algorithms import FCFS, Buddy, SJF, BF, WF, NF
from log import logger

'''
FCFS: First Come First Sever, 先到先服务算法
Buddy:我的算法
SJF:Short Job First, 短作业优先算法
BF: Best Fit, 最优适应算法
WF: Worst Fit, 最差适应算法
NF: Next Fit, 循环适应算法 
'''
# algorithms = [FCFS, Buddy, SJF, BF, WF, NF]
algorithms = [FCFS]
tasks = dataPrepare.read_and_createTasks(config.file_path)
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
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
from datetime import datetime




def read_data(algorithm_name, data_path):
    with open(os.path.join(data_path, f"{algorithm_name}_data.json"), 'r') as file:
        data = json.load(file)
    return pd.DataFrame([data])


# 绘制图表
def plot_data(df):
    # 将时间字符串转换为datetime对象
    df['time'] = pd.to_datetime(df['time'])

    # 设置图表大小
    plt.figure(figsize=(10, 6))

    # 绘制每个指标的图表
    for column in ['average_completion_time', 'number_of_free_cards', 'scheduling_efficiency', 'average_queue_time']:
        plt.plot(df['time'], df[column], label=column)

    # 设置图例
    plt.legend()

    # 设置标题和坐标轴标签
    plt.title('Algorithm Performance Over Time')
    plt.xlabel('Time')
    plt.ylabel('Value')

    # 保存图表
    plt.savefig(f"{algorithm_name}_performance.png")
    plt.show()


# 主函数
def main():
    algorithm_name = 'your_algorithm_name'  # 替换为你的算法名称
    data_path = config.experiment_data_path  # 替换为你的数据路径

    # 读取数据
    df = read_data(algorithm_name, data_path)

    # 绘制并保存图表
    plot_data(df)


if __name__ == "__main__":
    main()

