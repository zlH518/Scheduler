import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import config

def plot_data(algorithm_name):
    with open(os.path.join(config.experiment_data_path, f"{algorithm_name}_data.json"), 'r') as file:
        data = json.load(file)
    df = pd.DataFrame([data])

    for column in df.columns[1:]:
        plt.figure(figsize=(10, 6))
        plt.plot(df['time'][0], df[column][0], marker='o', linestyle='-', label=column)
        plt.title(f'{column} Over Time')
        plt.xlabel('Time')
        plt.ylabel(column)
        plt.legend()
        plt.grid(True)
        plt.savefig(os.path.join(config.experiment_data_path, f"{algorithm_name}_{column}.png"))
        plt.show()
        plt.close()
