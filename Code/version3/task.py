import glob
import pandas as pd
from log import logger
import config


class Task:
    completed_task_queue_time = []
    average_queue_time = 0
    Tasks = []
    TaskId = 0

    def __init__(self, create_time, start_time, cards, duration,
                 gpu_time, migration_cost, pre_queue_time):
        self.task_id = Task.TaskId
        self.create_time = create_time
        self.start_time = start_time
        self.cards = cards
        self.gpu_time = gpu_time
        self.duration_time = duration
        self.migration_cost = migration_cost
        self.pre_queue_time = pre_queue_time

        # real_parameter
        self.real_start_time = None

        Task.Tasks.append(self)
        Task.Tasks = sorted(Task.Tasks, key=lambda task: task.create_time)
        Task.TaskId += 1

    def __repr__(self):
        return (f"Task(task_id={self.task_id}, create_time={self.create_time}, "
                f"start_time={self.start_time}, cards={self.cards}, "
                f"duration_time={self.duration_time}, gpu_time={self.gpu_time}\n")

    @property
    def queue_time(self):
        return self._queue_time

    @queue_time.setter
    def queue_time(self, value):
        self._queue_time = value
        Task.completed_task_queue_time.append(value)

        valid_times = [t for t in Task.completed_task_queue_time if t is not None]
        if valid_times:
            Task.average_queue_time = sum(valid_times) / len(valid_times)
        else:
            Task.average_queue_time = 0

    @classmethod
    def reset(cls, file_path):
        cls.completed_task_queue_time.clear()
        cls.average_queue_time = 0
        cls.Tasks.clear()
        cls.TaskId = 0
        cls.read_and_createTasks(file_path)



    @classmethod
    def read_and_createTasks(cls,file_path):
        file_name = glob.glob(file_path)
        for file in file_name:
            try:
                data = pd.read_csv(file, usecols=['create_time', 'start_time', 'cards', 'gpu_time', 'duration_time', 'migration_cost', 'pre_queue_time'])
                logger.log(msg=str(f"file:{file} read success!"))
                for row in data.itertuples():
                    Task(create_time=row.create_time, start_time=row.start_time,
                         cards=row.cards, duration=row.duration_time,
                         gpu_time=row.gpu_time, migration_cost=row.migration_cost,
                         pre_queue_time=row.pre_queue_time)
            except Exception as e:
                print(f"file:{file}: {e}")
        logger.log(msg=f"all files was read done!")
        logger.log(msg=f"the number of task is {len(Task.Tasks)}")
        return True


if __name__ == '__main__':


    print(len(Task.Tasks))
    print(Task.completed_task_queue_time)
    print(Task.average_queue_time)
    print(Task.TaskId)

    Task.reset()
    Task.Tasks[0].queue_time = 10
    Task.Tasks[2].queue_time = 15

    print(len(Task.Tasks))
    print(Task.completed_task_queue_time)
    print(Task.average_queue_time)
    print(Task.TaskId)

    Task.reset()
    print(len(Task.Tasks))
    print(Task.completed_task_queue_time)
    print(Task.average_queue_time)
    print(Task.TaskId)

    for task in Task.Tasks:
        print(task)