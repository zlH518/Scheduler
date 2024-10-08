import pandas as pd
import numpy as np

import config
from log import logger
import os

def create_tasks():
    np.random.seed(config.random_seed)
    cards_values = config.cards_per_group
    cards_ratios = [16, 8, 4, 2]
    adjusted_ratios = [x * np.random.uniform(0.9, 1.1) for x in cards_ratios]
    total_ratio = sum(adjusted_ratios)
    cards_ratios = [x / total_ratio for x in adjusted_ratios]

    total_tasks = 50000
    counts = [int(total_tasks * ratio) for ratio in cards_ratios]
    cards_data = np.array([cards_values[i] for i in np.random.choice(len(cards_values), size=total_tasks, p=cards_ratios)])

    create_time = np.random.uniform(0, 3888000, total_tasks).astype(int)

    start_time = create_time + np.random.randint(1, 100, total_tasks)

    min_duration = 3600
    max_duration = 1296000
    duration_time = np.zeros(total_tasks, dtype=int)
    for i, cards in enumerate(cards_data):
        if np.random.rand() < 0.9:
            max_duration_for_card = max_duration // (8 - np.where(np.array(cards_values) == cards)[0][0] + 1)
            duration_time[i] = np.random.randint(min_duration, min(max_duration_for_card, max_duration))
        else:
            duration_time[i] = np.random.randint(min_duration, max_duration)

    gpu_time = cards_data * duration_time

    df = pd.DataFrame({
        'create_time': create_time,
        'start_time': start_time,
        'cards': cards_data,
        'gpu_time': gpu_time,
        'duration_time': duration_time
    })

    df.to_csv(os.path.join('C:\\Users\\Administrator\\Desktop\\IdsLab\任务\\SchedulerSystem\\Code\\version1\\data','tasks_data.csv'), index=False)
    logger.log("Data has been saved to tasks_data.csv")


# def create_node():
#     np.random.seed(config.random_seed)
#     cards_values = config.cards_per_group
#     cards_ratios = [16, 8, 4, 2, 1]
#     adjusted_ratios = [x * np.random.uniform(0.9, 1.1) for x in cards_ratios]
#     total_ratio = sum(adjusted_ratios)
#     cards_ratios = [x / total_ratio for x in adjusted_ratios]
#
#     total_tasks = 50000
#     counts = [int(total_tasks * ratio) for ratio in cards_ratios]
#     cards_data = np.array([cards_values[i] for i in np.random.choice(len(cards_values), size=total_tasks, p=cards_ratios)])
#
#     create_time = np.random.uniform(0, 3888000, total_tasks).astype(int)
#
#     start_time = create_time + np.random.randint(1, 100, total_tasks)
#
#     min_duration = 3600
#     max_duration = 1296000
#     duration_time = np.zeros(total_tasks, dtype=int)
#     for i, cards in enumerate(cards_data):
#         if np.random.rand() < 0.9:
#             max_duration_for_card = max_duration // (8 - np.where(np.array(cards_values) == cards)[0][0] + 1)
#             duration_time[i] = np.random.randint(min_duration, min(max_duration_for_card, max_duration))
#         else:
#             duration_time[i] = np.random.randint(min_duration, max_duration)
#
#     gpu_time = cards_data * duration_time
#
#     df = pd.DataFrame({
#         'create_time': create_time,
#         'start_time': start_time,
#         'cards': cards_data,
#         'gpu_time': gpu_time,
#         'duration_time': duration_time
#     })
#
#     df.to_csv(os.path.join('C:\\Users\\Administrator\\Desktop\\IdsLab\任务\\SchedulerSystem\\Code\\version1\\data','tasks_data.csv'), index=False)
#     logger.log("Data has been saved to tasks_data.csv")