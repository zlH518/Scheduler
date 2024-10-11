import os.path
from typing import Iterable
import config
from node import Node
from log import logger
import json
import copy
from task import Task
from itertools import combinations

class FCFS_With_migrate:
    def __init__(self):
        self.nodes = Node.Nodes      #拿到节点
        self.tasks = Task.Tasks      #拿到任务
        self.algorithm_name = 'FCFS_With_Migrate'
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

    def migrate(self, target, current_time):
        def find_movement_combinations(node_id, target_task):
            requirement_cards = target_task.cards
            current_node = self.nodes[node_id]
            current_used_cards = sum(task.cards for task in current_node.tasks)
            current_free_cards = config.cards_per_node - current_used_cards
            space_to_free = requirement_cards - current_free_cards

            if space_to_free <= 0:
                return None
            valid_combinations = None

            for r in range(1,len(current_node.tasks)+1):
                for combo in combinations(current_node.tasks, r):
                    total_space_free = sum(task.cards for task in combo)
                    if total_space_free >= space_to_free:   #满足条件1:释放之后空间足够了
                        # valid_combinations.append(combo)
                        #开始判断条件2:迁移出来的任务是否都有地方可以存放
                        copy_node = copy.deepcopy(self.nodes[:node_id]) + copy.deepcopy(self.nodes[node_id+1:])
                        remain_node = copy.deepcopy(copy_node)
                        flag = True
                        for item in combo:
                            placed = False
                            for node in sorted(remain_node):
                                if node.empty_cards >= item.cards:
                                    placed = True
                                    node.empty_cards -= item.cards
                                    break
                            if not placed:
                                flag = False
                                break
                        if flag:    #表示这个方案都满足条件，则选取代价最低的
                            if valid_combinations is None:
                                valid_combinations = combo
                            elif target_task.pre_queue_time >= sum(task.migration_cost for task in combo) and sum(task.migration_cost for task in combo)<sum(task.migration_cost for task in valid_combinations):
                                valid_combinations = combo
            return valid_combinations
            #现在就获取到了当前节点中收益最高的迁移方案

        #依次查找所有的节点，查找每个节点中收益最高的方案，再查找所有节点中收益最高的方案
        best_combination = None
        best_node = None
        if sum(node.empty_cards for node in self.nodes) < target.cards:
            return False
        for node in self.nodes:
            valid_combination = find_movement_combinations(node.node_id, target)
            if valid_combination is None:
                continue
            if best_combination is None:
                best_node = node
                best_combination = valid_combination
            else:
                if sum(task.migration_cost for task in best_combination) > sum(task.migration_cost for task in valid_combination):
                    best_combination = valid_combination
                    best_node = node
        if best_combination is not None:        #如果存在可以替换的方案，则开始替换
            #从目标节点挪出任务
            for task in best_combination:
                best_node.empty_cards += task.cards
                best_node.tasks.remove(task)
            #将目标任务放到节点中
            target.real_start_time = current_time
            target.queue_time = current_time - target.cards
            best_node.tasks.append(target)
            best_node.empty_cards -= target.cards
            #将挪出来的任务放置到其他节点中去
            remain_node = self.nodes[:best_node.node_id] + self.nodes[best_node.node_id+1:]
            flag = True
            for item in best_combination:
                for node in sorted(remain_node):
                    if node.empty_cards >= item.cards:
                        node.empty_cards -= item.cards
                        node.tasks.append(item)
                        break
            return True
        return False


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

            pass    #TODO:迁移策略的完善
            if len(wl) == 0:        #迁移没有收益
                pass
            else:                   #迁移可能有收益
                pass
                if self.migrate(wl[0], current_time):     #进行迁移
                    del wl[0]


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


if __name__ == '__main__':
    a=[1,2,3,4,5,6,7,8]
    for index, data in enumerate(a):
        if index == 3:
            del a[index]

    print(a)