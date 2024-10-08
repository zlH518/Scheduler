import pandas as pd
import glob
from task import Task
from log import logger
from datetime import datetime


def read_and_createTasks(file_path):
    file_name = glob.glob(file_path)
    tasks = []
    for file in file_name:
        try:
            data = pd.read_csv(file, usecols=['create_time', 'start_time', 'cards', 'gpu_time', 'duration_time'])
            logger.log(msg=str(f"file:{file} read success!"))
            for row in data.itertuples():
                tasks.append(
                    Task.create(create_time=row.create_time,start_time=row.start_time,
                                cards=row.cards, duration=row.duration_time, gpu_time=row.gpu_time))
        except Exception as e:
            print(f"file:{file}: {e}")
    logger.log(msg=f"all files was read done!")
    logger.log(msg=f"the number of task is {len(tasks)}")
    sorted(tasks, key=lambda x: x.create_time)
    return tasks

