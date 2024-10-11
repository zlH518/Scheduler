import os.path
from typing import Iterable
import config
from node import Node
from log import logger
import json
import copy
from task import Task
import pandas as pd

class FCFS:
    def __init__(self):
        self.nodes = Node.Nodes      #拿到节点
        self.tasks = Task.Tasks      #拿到任务
        self.algorithm_name = 'FCFS'
        self.time = []
        self.average_completion_time = []
        self.number_of_free_cards = []
        self.scheduling_efficiency = []
        self.average_queue_time = []
        self.completed_tasks = []
        self.average_duration_time = []
        print(len(Task.Tasks))

    def recoder(self):
        data = {
            'time': self.time,
            'average_completion_time': self.average_completion_time,
            'number_of_free_cards': self.number_of_free_cards,
            'scheduling_efficiency': self.scheduling_efficiency,
            'average_queue_time': self.average_queue_time,
            'average_duration_time': self.average_duration_time
        }
        json_data = json.dumps(data, indent=4)
        with open(os.path.join(config.experiment_data_path, f"{self.algorithm_name}_data.json"), 'w') as file:
            file.write(json_data)
        logger.log(f"Data has been recorded for {self.algorithm_name}")

    def save_new_data(self):
        tasks_data = [
            {
                'create_time': task.create_time,
                'start_time': task.start_time,
                'cards': str(task.cards),  # 将 cards 转换为字符串
                'gpu_time': task.gpu_time,
                'duration_time': task.duration_time,
                'migration_cost': task.migration_cost,
                'pre_queue_time': task.queue_time
            }
            for task in Task.Tasks
        ]
        df = pd.DataFrame(tasks_data)
        df.to_csv(config.new_data_file_path, index=False, sep=',')

    def addTask(self, current_time, task):
        node_index = None
        for index1, node in enumerate(sorted(self.nodes, reverse=True)):
            if node.empty_cards >= task.cards:
                node_index = node.node_id
                break
        if node_index is None:
            return False
        else:
            task.real_start_time = current_time
            task.queue_time = current_time - task.create_time
            print(task.queue_time)
            self.nodes[node_index].empty_cards -= task.cards
            self.nodes[node_index].tasks.append(task)
            return True

    def popTask(self, current_time):
        for index, node in enumerate(self.nodes):
            for index2, task in enumerate(node.tasks):
                if current_time - task.real_start_time >= task.duration_time:
                    node.empty_cards += task.cards                  #释放GPU
                    self.completed_tasks.append(task)
                    # print(str(task.task_id) + '号任务已被释放')
                    del node.tasks[index2]                          #删除任务


    def run(self):
        start_time = self.tasks[0].create_time
        current_time = start_time
        logger.log(f'start_time:{start_time}')
        index = 0
        wl = []
        recode_num = 0
        while len(self.completed_tasks) != len(list(self.tasks)):
            self.popTask(current_time)
            if index < len(self.tasks):
                while self.tasks[index].create_time <= current_time:
                    wl.insert(0, self.tasks[index])
                    index += 1
                    if index == len(self.tasks):
                        break
            if len(wl) == 0:
                current_time += config.step
                continue
            # logger.log(f'number of new task is {number_of_new_task}')
            recode_num += 1
            if recode_num % config.recode_num == 0:
                wl_temp = copy.deepcopy(wl)
            for index2 in range(len(wl) - 1, -1, -1):
                status = self.addTask(current_time, wl[index2])
                if status:  # 找到节点并放置
                    # print(str(wl[index2].task_id) + '任务已被放置')
                    del wl[index2]
                else:  # 找不到可用的节点
                    continue
            current_time += config.step
            if recode_num % config.recode_num == 0:
                # logger.log(f'{current_time} already recoded!')
                self.time.append(current_time)
                self.average_duration_time.append(
                    sum(task.duration_time for task in self.completed_tasks) / len(
                        self.completed_tasks) if len(self.completed_tasks) != 0 else 0)
                self.average_completion_time.append(
                    sum(task.queue_time + task.duration_time for task in self.completed_tasks) / len(
                        self.completed_tasks) if len(self.completed_tasks) != 0 else 0)
                self.number_of_free_cards.append(sum(node.empty_cards for node in self.nodes))
                self.scheduling_efficiency.append(float(
                    (sum(task.cards for task in wl_temp) - sum(task.cards for task in wl)) / sum(
                        task.cards for task in wl_temp)) if len(wl_temp) != 0 else 0.0)
                self.average_queue_time.append(
                    sum(task.queue_time for task in self.completed_tasks) / len(self.completed_tasks) if len(
                        self.completed_tasks) != 0 else 0)
        print(f'completed_tasks:{len(self.completed_tasks)}')
        print(f'tasks:{len(self.tasks)}')
        assert len(self.completed_tasks) == len(self.tasks)
        assert sum(node.empty_cards for node in self.nodes) == config.node_num * config.cards_per_node
        self.time.append(current_time)
        self.average_duration_time.append(
            sum(task.duration_time for task in self.completed_tasks) / len(
                self.completed_tasks) if len(self.completed_tasks) != 0 else 0)
        self.average_completion_time.append(
            sum(task.queue_time + task.duration_time for task in self.completed_tasks) / len(
                self.completed_tasks) if len(self.completed_tasks) != 0 else 0)
        self.number_of_free_cards.append(sum(node.empty_cards for node in self.nodes))
        self.scheduling_efficiency.append(float(
            (sum(task.cards for task in wl_temp) - sum(task.cards for task in wl)) / sum(
                task.cards for task in wl_temp)) if len(wl_temp) != 0 else 0.0)
        self.average_queue_time.append(
            sum(task.queue_time for task in self.completed_tasks) / len(self.completed_tasks) if len(
                self.completed_tasks) != 0 else 0)
        self.recoder()
        self.save_new_data()


if __name__ == '__main__':
    a=[1,2,3,4,5,6,7,8]
    for index, data in enumerate(a):
        if index == 3:
            del a[index]

    print(a)