import config
import json
import os
import pandas as pd
import matplotlib.pyplot as plt



def plot_data(algorithm_names):
    plt.figure(figsize=(10, 6))

    # 读取所有算法的数据
    all_data = []
    for algorithm_name in algorithm_names:
        with open(os.path.join(config.experiment_data_path, f"{algorithm_name}_data.json"), 'r') as file:
            data = json.load(file)
            all_data.append(data)

    # 将所有数据转换为DataFrame
    df = pd.DataFrame(all_data)

    # 遍历每个指标进行绘图
    for column in ['average_completion_time', 'number_of_free_cards', 'scheduling_efficiency', 'average_queue_time']:
        plt.figure(figsize=(10, 6))
        for index, algorithm_name in enumerate(algorithm_names):
            plt.plot(df['time'][index], df[column][index], linestyle='-', label=algorithm_name)
        plt.title(f'{column} Over Time')
        plt.xlabel('Time')
        plt.ylabel(column)
        plt.legend()
        # plt.grid(True)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.savefig(os.path.join(config.experiment_data_path, f"{column}.png"))
        plt.show()
        plt.close()

