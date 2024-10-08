from algorithms import BaseAlgorithm
import config
from log import logger
import copy
import heapq


class FCFS(BaseAlgorithm):
    def __init__(self):
        super().__init__()
        self.algorithm_name = 'FCFS'

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
        start_time = tasks[0].create_time       #整个模拟的开始时间
        current_time = start_time - 1               #current_time作为时间指针
        logger.log('-'*20+f'{self.algorithm_name} Begin!!!!'+'-'*20)
        index = 0                               #作为所有任务的指针
        wl = []                                 #到达时间为优先级的优先队列wl
        recode_num = 0                          #记录周期定时器
        while len(self.completed_tasks) != len(list(tasks)):        #只要还有任务没有完成则继续
            current_time += config.step                   #时间自增
            logger.log(f"{current_time}: {len(self.completed_tasks)}/{len(list(tasks))}")       #log日志记录一下
            number_of_new_task = 0
            while index < len(tasks) and tasks[index].create_time <= current_time:     #查看是否有任务到来，有的话就放到wl中
                heapq.heappush(wl, (tasks[index].create_time,tasks[index]))
                number_of_new_task += 1
                index += 1
            for index2 in range(len(wl) - 1, -1, -1):               #从队列中按照时间取任务，查找可用的节点
                status = self.addTask(current_time, wl[index2])
                if status:  # 找到节点并放置
                    del wl[index2]
                else:  # 找不到可用的节点
                    continue




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
