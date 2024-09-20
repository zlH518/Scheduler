from typing import Iterable
import config
import node
from log import logger


class BaseAlgorithm:
    def __init__(self):
        self.nodes = [node.BaseNode(config.cards_per_node) for _ in range(config.node_num)]
        self.algorithm_name = 'BaseAlgorithm'
    def addTask(self, current_time):
        logger.log(f"addTask function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')

    def popTask(self, current_time):
        logger.log(f"popTask function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')

    def run(self, tasks: Iterable):
        logger.log(f"run function need implement in {self.algorithm_name}")
        raise NotImplementedError('Need to implement')


class FCFS(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'First Come First Sever'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: Iterable):
        print('ok')


class Buddy(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Buddy'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: Iterable):
        print('ok')


class SJF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Short Job First'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: Iterable):
        print('ok')


class BF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Best First'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: Iterable):
        print('ok')


class WF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Worst First'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    def run(self, tasks: Iterable):
        print('ok')


class NF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Next First'

    def addTask(self, current_time):
        print('ok')

    def popTask(self, current_time):
        print('ok')

    # def run(self, tasks: Iterable):
    #     print('ok')
