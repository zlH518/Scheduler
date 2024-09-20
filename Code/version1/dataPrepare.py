import pandas as pd
import glob
from task import Task
import tqdm
from log import logger


def read_and_createTasks(file_path):
    file_name = glob.glob(file_path)
    tasks = []

    for file in file_name:
        try:
            data = pd.read_csv(file, usecols=['submit_time', 'start_time', 'gpu_num',
                                              'duration', 'gpu_time'])
            logger.log(msg=str(f"file:{file} read success!"))
            for row in tqdm.tqdm(data.itertuples()):
                tasks.append(
                    Task.create(create_time=row[0], start_time=row[1],
                                cards=row[2], duration=row[3], gpu_time=row[4]))
        except Exception as e:
            print(f"file:{file}: {e}")
    logger.log(msg=f"all files was read done!")
    logger.log(msg=f"the number of task is {len(tasks)}")
    return tasks
