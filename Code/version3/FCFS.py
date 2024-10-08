import os.path
from typing import Iterable
import config
from node import Node
from log import logger
import json
import copy
from task import Task

class FCFS:
    def __init__(self):
        self.nodes = copy.deepcopy(Node.Nodes)      #拿到节点
        self.tasks = copy.deepcopy(Task.Tasks)      #拿到任务
        self.algorithm_name = 'FCFS'
        self.time = []
        self.average_completion_time = []
        self.number_of_free_cards = []
        self.scheduling_efficiency = []
        self.average_queue_time = []
        self.completed_tasks = []
        print(len(Task.Tasks))

    def recoder(self):
        data = {
            'time': self.time,
            'average_completion_time': self.average_completion_time,
            'number_of_free_cards': self.number_of_free_cards,
            'scheduling_efficiency': self.scheduling_efficiency,
            'average_queue_time': self.average_queue_time
        }
        json_data = json.dumps(data, indent=4)
        with open(os.path.join(config.experiment_data_path, f"{self.algorithm_name}_data.json"), 'w') as file:
            file.write(json_data)
        logger.log(f"Data has been recorded for {self.algorithm_name}")


    def addTask(self, current_time, task):
        def getEmptyNode(need: int):
            if next((node for node in self.nodes if node.remainCards >= need), None) is not None:
                index = next((index for index, node in enumerate(self.nodes) if node.remainCards >= need), None)
                return index
            else:
                return None

        node_index = getEmptyNode(task.cards)
        if node_index is None:
            return False
        else:
            task.real_start_time = current_time
            task.queue_time = current_time - task.create_time
            self.nodes[node_index].remainCards -= task.cards
            self.nodes[node_index].tasks.append(task)
            return True

    def popTask(self, current_time):
        for index, node in enumerate(self.nodes):
            for index2, task in enumerate(node.tasks):
                if current_time - task.real_start_time >= task.duration_time:
                    node.remainCards += task.cards
                    del node.tasks[index2]
                    task.real_end_time = current_time
                    self.completed_tasks.append(task)

    def run(self, tasks: list):
        start_time = tasks[0].create_time
        self.up_time = 0
        current_time = start_time
        logger.log(f'start_time:{start_time}')
        index = 0
        wl = []
        recode_num = 0
        while len(self.completed_tasks) != len(list(tasks)):
            # if len(self.completed_tasks) == 30:
            #     input()
            logger.log(f"{current_time}: {len(self.completed_tasks)}/{len(list(tasks))}")
            self.popTask(current_time)
            self.up_time += 1
            number_of_new_task = 0
            if index < len(tasks):
                while tasks[index].create_time <= current_time:
                    wl.insert(0, tasks[index])
                    number_of_new_task += 1
                    index += 1
                    if index == len(tasks):
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
                    del wl[index2]
                else:  # 找不到可用的节点
                    continue
            current_time += config.step
            if recode_num % config.recode_num == 0:
                # logger.log(f'{current_time} already recoded!')
                self.time.append(current_time)
                self.average_completion_time.append(
                    sum(task.queue_time + task.duration_time for task in self.completed_tasks) / len(
                        self.completed_tasks) if len(self.completed_tasks) != 0 else 0)
                self.number_of_free_cards.append(sum(node.remainCards for node in self.nodes))
                self.scheduling_efficiency.append(float(
                    (sum(task.cards for task in wl_temp) - sum(task.cards for task in wl)) / sum(
                        task.cards for task in wl_temp)) if len(wl_temp) != 0 else 0.0)
                self.average_queue_time.append(
                    sum(task.queue_time for task in self.completed_tasks) / len(self.completed_tasks) if len(
                        self.completed_tasks) != 0 else 0)
        self.recoder()