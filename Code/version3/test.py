import copy
import config
from itertools import combinations


def find_movement_combinations(node_id, requirement_cards):
    current_node = nodes[node_id]
    current_used_cards = sum(task.cards for task in current_node.tasks)
    current_free_cards = config.cards_per_node - current_used_cards
    space_to_free = requirement_cards - current_free_cards

    if space_to_free <= 0:      #表明不需要迁移就可以放进去
        return None
    valid_combinations = []

    for r in range(1, len(current_node.tasks) + 1):
        for combo in combinations(current_node.tasks, r):
            total_space_free = sum(task.cards for task in combo)
            if total_space_free >= space_to_free:  # 满足条件1:释放之后空间足够了
                # valid_combinations.append(combo)
                # 开始判断条件2:迁移出来的任务是否都有地方可以存放
                copy_node = copy.deepcopy(nodes[:node_id]) + copy.deepcopy(nodes[node_id + 1:])
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
                if flag:
                    valid_combinations.append(combo)
    return valid_combinations


class Task:
    def __init__(self, task_id, cards):
        self.task_id = task_id  # 任务的唯一标识符
        self.cards = cards  # 任务占用的空间

    def __repr__(self):
        return f"Task(id={self.task_id}, space={self.cards})"


# 定义 Node 类，包含任务列表
class Node:
    def __init__(self, node_id):
        self.node_id = node_id  # 节点的唯一标识符
        self.tasks = []  # 存储当前节点的任务
        self.empty_cards = config.cards_per_node

    def add_task(self, tasks):
        for task in tasks:
            self.tasks.append(task)  # 添加任务到节点
            self.empty_cards -= task.cards

    def __lt__(self, other):
        return self.empty_cards < other.empty_cards

nodes = []
node1 = Node(0)
node1.add_task([Task(task_id=i, cards=cards) for i, cards in enumerate([1, 2, 2, 2])])
nodes.append(node1)

node2 = Node(1)
node2.add_task([Task(task_id=i, cards=cards) for i, cards in enumerate([4, 2])])
nodes.append(node2)

node3 = Node(2)
node3.add_task([Task(task_id=i, cards=cards) for i, cards in enumerate([2, 2, 2, 1])])
nodes.append(node3)

node4 = Node(3)
node4.add_task([Task(task_id=i, cards=cards) for i, cards in enumerate([2, 2, 2, 1])])
nodes.append(node4)
if __name__ == '__main__':
    combos = find_movement_combinations(0,4)
    for index, combo in enumerate(combos, 1):
        print(combo)






