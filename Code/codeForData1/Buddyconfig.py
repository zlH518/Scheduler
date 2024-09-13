import numpy as np
from typing import List, Iterable

config = {
    'dataPath': "C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum': 100,
    'cardsPerNode': 8,
    'tao': 5,
    'GNum': 5,
    'theta4': [0.5, 0.5, 0.5, 0.5],
    'theta5': [0.5, 0.5, 0.5, 0.5, 0.5],
    'cardsProcess5': [1, 2, 4, 6, 8],
    'cardsProcess4': [1, 2, 4, 8],
    'T': 1000
}
indexMap = {
    5: lambda item: item // 2,
    4: lambda item: item // 2 if item != 8 else 3
}
indexOrder = indexMap.get(config['GNum'])

def getOrder(item):
    return indexOrder(item)


def getNext(item):
    index = indexOrder(item) + 1
    if config['GNum'] == 5:
        if index > 4:
            return None
    elif config['GNum'] == 4:
        if index > 3:
            return None
    return config[f'cardsProcess{config["GNum"]}'][index]


def getFront(item):
    index = indexOrder(item) - 1
    if index < 0:
        return None
    return config[f'cardsProcess{config["GNum"]}'][index]


class Task:
    TaskId = 0
    def __init__(self, startTime, schedulingTime, createTime, duration, cards):
        self.startTime = startTime
        self.schedulingTime = schedulingTime
        self.createTime = createTime
        self.durationTime = duration
        self.cards = cards
        self.flagTime = None
        self.completeTime = None
        self.taskId = Task.TaskId
        Task.TaskId += 1

    def __repr__(self):
        return (f"Task(createTime:{self.createTime}, startTime={self.startTime}, "
                f"schedulingTime:{self.schedulingTime},durationTime:{self.durationTime}, "
                f"cards:{self.cards})\n")


class ALLTasks:
    def __init__(self, index: list, data: list):
        self.index = index
        self.allTask = data
        startTime = np.array([task.startTime for task in data])
        schedulingTime = np.array([task.schedulingTime for task in data])
        createTime = np.array([task.createTime for task in data])
        duration = np.array([task.durationTime for task in data])
        cards = np.array([task.cards for task in data])
        endTime = np.array([task.startTime + task.durationTime for task in data])
        self.matrix = np.column_stack((startTime, schedulingTime, createTime, duration, cards, endTime))

    def __len__(self):
        return self.matrix.shape[0]


class Node:
    NodeId = 0

    def __init__(self, cardsPerNode: int):
        self.nodeId = Node.NodeId
        Node.NodeId += 1
        self.cards = cardsPerNode
        self.tasks = []
        self.unpackagedCards = cardsPerNode
        self.unuesdCards = cardsPerNode


nodes=[Node(config['cardsPerNode']) for _ in range(config['nodeNum'])]

def getNodeStatus(nodes: Iterable[Node]):
    def nodeStatus(node: Node):
        print(f'nodeId:{node.nodeId}, cards:{node.cards}, unusedCards:{node.unuesdCards}, unpackagedCards:{node.unpackagedCards}\n')

    for node in nodes:
        nodeStatus(node)
    return None


class Package:
    def __init__(self, cardsPerPackage: int, nodeId: int):
        self.cards = cardsPerPackage
        self.nodeId = nodeId
        self.task = None

    def __len__(self):
        return self.cards


class Group:
    GROUPID = 0

    def __init__(self, cardsPerPackage: int, nodes: Iterable[Node], theta: float):
        self.cardsPerPackage = cardsPerPackage
        self.emptyPackage = []
        self.usedPackage = []
        self.theta = theta
        self.completedTask = []
        self.durationTime = []
        self.groupid = Group.GROUPID
        Group.GROUPID += 1
        for index, node in enumerate(nodes):
            while node.unpackagedCards >= self.cardsPerPackage:
                self.emptyPackage.append(Package(self.cardsPerPackage, node.nodeId))
                node.unpackagedCards -= self.cardsPerPackage
        self.emptyRate = float(len(self.emptyPackage) / (len(self.emptyPackage) + len(self.usedPackage)))
        print(f'create Group{self.GROUPID} success! \n '
              f'cardsPerPackage:{cardsPerPackage}, nodesNum:{len(nodes)}, theta:{theta}\n')

    def popTask(self, currentTime):
        #查看所有用的package，中是否有需要释放的task
        num = 0
        for package in self.usedPackage:
            nodeId=package.nodeId
            if currentTime - package.task.flagTime >= package.task.durationTime:
                nodes[nodeId].unuesdCards += package.task.cards
                index = next((i for i, task in enumerate(nodes[nodeId].tasks) if task.taskId == package.task.taskId), None)
                del nodes[nodeId].tasks[index]
                self.usedPackage.remove(package)
                self.completedTask.append(package.task.taskId)
                self.durationTime.append(currentTime - package.task.createTime)
                package.task=None
                self.emptyPackage.append(package)
                num += 1
        return num

    def info(self):
        return  f'{self.groupid}:{self.emptyRate}'


    def getEmptyPackage(self, need):
        if len(self.emptyPackage) == 0:
            return None
        else:
            '''这里或许可以做更多优化，使得分配的package更优'''
            return self.emptyPackage[0]

    def putTask(self, task: Task, currentTime: int):
        package = self.getEmptyPackage(task.cards)
        del self.emptyPackage[0]
        task.flagTime = currentTime
        nodeId=package.nodeId
        package.task = task
        nodes[nodeId].unuesdCards -= task.cards
        nodes[nodeId].tasks.append(task)
        self.usedPackage.append(package)
        return True

    def schedule(self):
        # 创建一个字典来存储相同nodeId的packages
        packagesByNode = {}
        for package in self.emptyPackage:
            if package.nodeId not in packagesByNode:
                packagesByNode[package.nodeId] = [package]
            else:
                # 如果已经存在相同nodeId的package，则先收集起来
                packagesByNode[package.nodeId].append(package)

        # 更新emptyPackage列表，只包含存在一个package的packageByNode,并从字典中去除
        self.emptyPackage=[]
        for item in packagesByNode.values():
            if len(item) == 1:
                self.emptyPackage.append(item[0])
            else:       #这里需要根据
                pass


        # # 重新计算emptyRate
        # group.emptyRate = float(len(group.emptyPackage) / (len(group.emptyPackage) + len(group.usedPackage)))


class Groups:
    def __init__(self, cardsPerNode: int, nodes: Iterable[Node]):
        self.cardsPerNode = cardsPerNode
        self.Gnum = config['GNum']
        self.G = []
        if self.Gnum == 5:
            self.theta = config['theta5']
            self.cardsProcess = config['cardsProcess5']
        elif self.Gnum == 4:
            self.theta = config['theta4']
            self.cardsProcess = config['cardsProcess4']
        avgNum = len(nodes) // self.Gnum
        for i in range(self.Gnum):
            self.G.append(Group(cardsPerPackage=self.cardsProcess[i], nodes=nodes[i * avgNum:(i + 1) * avgNum] \
                if i != self.Gnum - 1 else nodes[i * avgNum:], theta=self.theta[i]))
        #查找所有nodes中是否还有unpackagedCards，按照8，6，4，2，1进行打包放置到对应的组中
        for node in nodes:
            while node.unpackagedCards != 0:
                for cards in reversed(self.cardsProcess):
                    if node.unpackagedCards % int(cards) == 0:
                        self.G[indexOrder(int(cards))].emptyPackage.append(Package(int(cards), node.nodeId))
                        node.unpackagedCards -= int(cards)
                        break
                    else:
                        continue

    def __getitem__(self, item):
        group = self.G[indexOrder(item)]
        while group.getEmptyPackage(item) is None:
            item = getNext(item)
            if item is not None:
                group = self.G[indexOrder(item)]
            else:
                return None
        return group

    def popTask(self,currentTime):
        sum = 0
        for group in self.G:
             sum += group.popTask(currentTime)
        return sum

    def info(self):
        # durationTime=[]
        # for group in self.G:
        #     durationTime += group.info()
        # return durationTime
        str=''
        for group in self.G:
            str =str + ' ' + group.info()
        return str+'\n'

    def durationTime(self):
        durationTime=[]
        for group in self.G:
            durationTime += group.durationTime
        return np.mean(np.array(durationTime))

    def scheduleResources(self):
        for group in reversed(self.G[:-1]):
            if group.emptyRate >= group.theta:
                group.schedule()