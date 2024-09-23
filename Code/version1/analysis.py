import matplotlib.pyplot as plt
import pandas as pd
import os
import config


def plot_histograms(tasks):
    data = {
        'create_time': [task.create_time for task in tasks],
        'start_time': [task.start_time for task in tasks],
        'cards': [task.cards for task in tasks],
        'gpu_time': [task.gpu_time for task in tasks],
        'duration_time': [task.duration_time for task in tasks]
    }

    df = pd.DataFrame(data)

    plt.figure(figsize=(15, 10))

    fig, axs = plt.subplots(2, 3, figsize=(15, 10))

    attributes = ['create_time', 'start_time', 'cards', 'gpu_time', 'duration_time']
    for i, attr in enumerate(attributes):
        axs[i // 3, i % 3].hist(df[attr], bins=20, color='skyblue', edgecolor='black')
        axs[i // 3, i % 3].set_title(f'Distribution of {attr}')
        axs[i // 3, i % 3].set_xlabel(attr)
        axs[i // 3, i % 3].set_ylabel('Frequency')

    # plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(config.analysis_path, "analysis.png"))
    plt.close()
