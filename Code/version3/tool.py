import config
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import PercentFormatter

palette = sns.color_palette("Set2")


def plot_data(algorithm_names):
    plt.figure(figsize=(10, 6))
    all_data = []
    for algorithm_name in algorithm_names:
        with open(os.path.join(config.experiment_data_path, f"{algorithm_name}_data.json"), 'r') as file:
            data = json.load(file)
            all_data.append(data)

    df = pd.DataFrame(all_data)

    #画三个时间
    line_styles = ['-', '--', ':']  # 实线、虚线、点线
    plt.figure(figsize=(10, 6))
    for index, algorithm_name in enumerate(algorithm_names):
        plt.plot(df['time'][index], df['average_completion_time'][index], linestyle=line_styles[0],
                 color=palette[index],
                 label=algorithm_name if index == 0 else "")
        plt.plot(df['time'][index], df['average_queue_time'][index], linestyle=line_styles[1], color=palette[index],
                 label="")
        plt.plot(df['time'][index], df['average_duration_time'][index], linestyle=line_styles[2], color=palette[index],
                 label="")

    plt.title('Metrics Over Time')
    plt.xlabel('Time')
    plt.ylabel('Metrics Over Time')

    # 添加指标线型图例
    handles = [
        plt.Line2D([0], [0], color='black', linestyle=line_styles[0], label='Average Completion Time'),
        plt.Line2D([0], [0], color='black', linestyle=line_styles[1], label='Average Queue Time'),
        plt.Line2D([0], [0], color='black', linestyle=line_styles[2], label='Average Duration Time')
    ]
    line_meaning = plt.legend(handles=handles, loc='upper left', title='meaning of line')

    color_handles = [plt.Line2D([0], [0], color=palette[i], label=algorithm_names[i]) for i in
                     range(len(algorithm_names))]
    plt.legend(handles=color_handles, loc='upper right', title='Algorithms', bbox_to_anchor=(0, -0.3))

    plt.gca().add_artist(line_meaning)
    # plt.gca().add_artist(color_meaning)

    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.savefig(os.path.join(config.experiment_data_path, "Metrics.png"))
    plt.show()
    plt.close()

    #画free_cards
    plt.figure(figsize=(10, 6))
    for index, algorithm_name in enumerate(algorithm_names):
        plt.plot(df['time'][index], df['number_of_free_cards'][index], linestyle=line_styles[0],
                 color=palette[index],
                 label=algorithm_name if index == 0 else "")

    plt.title('Number of Free Cards')
    plt.xlabel('Time')
    plt.ylabel('number of free cards')

    plt.legend(loc='upper right')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.savefig(os.path.join(config.experiment_data_path, "Free Cards.png"))
    plt.show()
    plt.close()


    #画利用率
    plt.figure(figsize=(10, 6))
    for index, algorithm_name in enumerate(algorithm_names):
        plt.plot(df['time'][index], df['scheduling_efficiency'][index], linestyle=line_styles[0],
                 color=palette[index],
                 label=algorithm_name if index == 0 else "")

    plt.title('Scheduling Efficiency')
    plt.xlabel('Time')
    plt.ylabel('Precent')
    plt.gca().yaxis.set_major_formatter(PercentFormatter(1))

    plt.legend(loc='upper right')
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.savefig(os.path.join(config.experiment_data_path, "Scheduling Efficiency.png"))
    plt.show()
    plt.close()



