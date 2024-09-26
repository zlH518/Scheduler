import os.path
from typing import Iterable
import config
from node import BaseNode
from log import logger
import json
from group import Group, Package
import copy


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
            'average_queue_time': self.average_queue_time
        }
        json_data = json.dumps(data, indent=4)
        with open(os.path.join(config.experiment_data_path, f"{self.algorithm_name}_data.json"), 'w') as file:
            file.write(json_data)
        logger.log(f"Data has been recorded for {self.algorithm_name}")


class FCFS(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'First Come First Sever'

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


class Buddy(BaseAlgorithm):

    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Buddy'
        self.groups = self.groupsInit()
        self.up_time = 0

    def groupsInit(self):
        G = []
        avgNum = len(self.nodes) // config.group_num
        for i in range(config.group_num):
            G.append(Group(cards_per_package=config.cards_per_group[i], theta=config.theta_per_group[i]))
        # 给每个group初始化Package
        for i in range(config.group_num):
            start_index = i * avgNum
            end_index = (i + 1) * avgNum if i < config.group_num - 1 else len(self.nodes)
            for node in self.nodes[start_index:end_index]:
                unused_cards = node.cards
                while unused_cards >= config.cards_per_group[i]:
                    G[i].package.append(Package(config.cards_per_group[i], node.nodeId))
                    unused_cards -= config.cards_per_group[i]
                if unused_cards == 2:
                    G[1].package.append(Package(config.cards_per_group[1], node.nodeId))
        return G

    def addTask(self, current_time, task):

        def getGroup(need: int):
            index = int(need / 2)
            group_possible = self.groups[index]
            while group_possible.getEmptyPackage() is None:
                index = index + 1
                if index >= config.group_num:
                    return None
                group_possible = self.groups[index]
            return group_possible

        group = getGroup(task.cards)
        # if current_time == 712:
        #     input()
        if group is None:
            return False
        else:
            available_package_index = group.getEmptyPackage()
            task.real_start_time = current_time
            task.queue_time = current_time - task.create_time
            # 找到资源了，接下来要对package查看是否需要拆分
            # 1.不需要拆分，则直接补充信息记录信息
            if group.package[available_package_index].cards == task.cards:
                group.package[available_package_index].task.append(task)
            # 2.这个Package太大了，需要对这个Package进行拆分
            else:
                package = group.package[available_package_index]
                unpackagedcards = package.cards
                del group.package[available_package_index]
                new_package = Package(cards_per_package=task.cards, node_index=package.nodeId)
                new_package.task = [task]
                group = self.groups[int(task.cards / 2)]
                group.package.append(new_package)
                unpackagedcards -= task.cards
                while unpackagedcards != 0:
                    temp = Package(cards_per_package=self.groups[int(unpackagedcards / 2)].cards_per_package,
                                   node_index=package.nodeId)
                    self.groups[int(unpackagedcards / 2)].package.append(temp)
                    unpackagedcards -= self.groups[int(unpackagedcards / 2)].cards_per_package
            return True

    def up_pieces(self):
        for group in self.groups:
            empty_package_by_nodeId = {}
            for index2 in range(len(group.package) - 1, -1, -1):
                if len(group.package[index2].task) == 0:
                    if group.package[index2].nodeId not in empty_package_by_nodeId:
                        empty_package_by_nodeId[group.package[index2].nodeId] = []
                    empty_package_by_nodeId[group.package[index2].nodeId].append(group.package[index2])
                    del group.package[index2]

            for node_id, item in empty_package_by_nodeId.items():
                all_cards = sum(package.cards for package in item)
                while all_cards != 0:
                    position_index = None
                    for index in range(len(config.cards_per_group) - 1, -1, -1):
                        if config.cards_per_group[index] <= all_cards:
                            position_index = index
                            break
                    new_package = Package(cards_per_package=config.cards_per_group[position_index],
                                          node_index=node_id)
                    self.groups[position_index].package.append(new_package)
                    all_cards -= new_package.cards


    def popTask(self, current_time):
        # 对每个group的ackage中的任务进行检查，时间到了就释放任务，然后对nodeId相同的package进行汇聚转移
        for group in self.groups:
            flag = False
            for package in group.package:
                if len(package.task) == 0:
                    continue
                if current_time - package.task[0].real_start_time >= package.task[0].duration_time:
                    task = package.task[0]
                    package.task = []
                    task.real_end_time = current_time
                    self.completed_tasks.append(task)
                    flag = True
            if flag:
                empty_package_by_nodeId = {}
                for index2 in range(len(group.package) - 1, -1, -1):
                    if len(group.package[index2].task) == 0:
                        if group.package[index2].nodeId not in empty_package_by_nodeId:
                            empty_package_by_nodeId[group.package[index2].nodeId] = []
                        empty_package_by_nodeId[group.package[index2].nodeId].append(group.package[index2])
                        del group.package[index2]

                for node_id, item in empty_package_by_nodeId.items():
                    all_cards = sum(package.cards for package in item)
                    while all_cards != 0:
                        position_index = None
                        for index in range(len(config.cards_per_group) - 1, -1, -1):
                            if config.cards_per_group[index] <= all_cards:
                                position_index = index
                                break
                        new_package = Package(cards_per_package=config.cards_per_group[position_index],
                                              node_index=node_id)
                        self.groups[position_index].package.append(new_package)
                        all_cards -= new_package.cards

    def run(self, tasks: list):
        start_time = tasks[0].create_time
        self.up_time = 0
        current_time = start_time
        logger.log(f'start_time:{start_time}')
        index = 0
        wl = []
        recode_num = 0
        while len(self.completed_tasks) != len(list(tasks)):
            # if len(self.completed_tasks) == 18:
            #     input()
            # if current_time == 1012:
            #     input()
            logger.log(f"{current_time}: {len(self.completed_tasks)}/{len(list(tasks))}")
            self.popTask(current_time)
            self.up_time += 1
            if self.up_time >= config.up_time:
                self.up_time = 0
                self.up_pieces()
            number_of_new_task = 0
            if index < len(tasks):
                while tasks[index].create_time <= current_time:
                    wl.insert(0, tasks[index])
                    # if index == 8:
                    #     input()
                    number_of_new_task += 1
                    index += 1
                    if index == len(tasks):
                        break
            if len(wl) == 0:
                current_time += config.step
                continue
            # logger.log(f'number of new task is {number_of_new_task}')
            recode_num += 1
            if recode_num % config.recode_num == 0:  # TODO用深拷贝
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
                self.number_of_free_cards.append(sum(sum(package.cards if len(package.task) == 0 else 0 for package in group.package) for group in self.groups))
                self.scheduling_efficiency.append(float(
                    (sum(task.cards for task in wl_temp) - sum(task.cards for task in wl)) / sum(
                        task.cards for task in wl_temp)) if len(wl_temp) != 0 else 0.0)
                self.average_queue_time.append(
                    sum(task.queue_time for task in self.completed_tasks) / len(self.completed_tasks) if len(
                        self.completed_tasks) != 0 else 0)
        self.recoder()


class SJF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Short Job First'

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
        self.up_time = start_time
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


class BF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Best First'

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
        self.up_time = start_time
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


class WF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Worst First'

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
        self.up_time = start_time
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


class NF(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'Next First'

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
        self.up_time = start_time
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
