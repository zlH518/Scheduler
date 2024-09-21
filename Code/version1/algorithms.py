from typing import Iterable
import config
from node import BaseNode
from log import logger
import json


class BaseAlgorithm:
    def __init__(self):
        self.nodes = [BaseNode(config.cards_per_node) for _ in range(config.node_num)]
        self.algorithm_name = 'BaseAlgorithm'
        self.time = []
        self.average_completion_time = []
        self.number_of_free_cards = []
        self.scheduling_efficiency = []
        self.average_queue_time = []
        self.completed_tasks = []

    def addTask(self, current_time, task):
        logger.log(f"addTask function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')

    def popTask(self, current_time):
        logger.log(f"popTask function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')

    def run(self, tasks: list):
        logger.log(f"run function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')

    def recoder(self):
        data = {
            'time': self.time,
            'average_completion_time': self.average_completion_time,
            'number_of_free_cards': self.number_of_free_cards,
            'scheduling_efficiency': self.scheduling_efficiency,
            'average_queue_time': self.average_queue_time,
            'completed_tasks': self.completed_tasks
        }
        json_data = json.dumps(data, indent=4)
        with open(f"{self.algorithm_name}_data.json", 'w') as file:
            file.write(json_data)
        logger.log(f"Data has been recorded for {self.algorithm_name}")


class FCFS(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'First Come First Sever'
        self.current_time = 0

    def addTask(self, current_time, task):
        def getEmptyNode(need: int):
            if next((node for node in self.nodes if node.remainCards >= need), None) is not None:
                index = next((index for index, node in enumerate(self.nodes) if node.remainCards >= need), None)
                return index
            else:
                return None

        flag, index = self.getEmptyNode(task.cards)
        if flag is None:
            return False
        if flag == 1:
            node = self.usedNodes[index]
            del self.usedNodes[index]
        else:
            node = self.emptyNodes[index]
            del self.emptyNodes[index]
        task.flagTime = currentTime
        node.remainCards -= task.cards
        node.tasks.append(task)
        self.usedNodes.append(node)
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
        start_time = min(tasks, key=lambda x: x.create_time)
        current_time = start_time
        index = 0
        wl = []
        while len(self.completed_tasks) != len(list(tasks)):
            self.popTask(current_time)
            while tasks[index].create_time <= current_time:
                wl.append(tasks[index])
                index += 1
            for task in wl:
                status = self.addTask(current_time, task)


class Buddy(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Buddy'

    def addTask(self, current_time, task):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: list):
        print('ok')


class SJF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Short Job First'

    def addTask(self, current_time, task):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: list):
        print('ok')


class BF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Best First'

    def addTask(self, current_time, task):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: list):
        print('ok')


class WF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Worst First'

    def addTask(self, current_time, task):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: list):
        print('ok')


class NF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Next First'

    def addTask(self, current_time, task):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: list):
        print('ok')
