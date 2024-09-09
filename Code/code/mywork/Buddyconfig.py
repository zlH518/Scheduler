import numpy as np
from typing import List,Iterable

config = {
    'dataPath': "C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum': 50,
    'cardsPerNode': 8,
    'tao': 5,
    'GNum': 5,
    'theta4': [0.5, 0.5, 0.5, 0.5],
    'theta5': [0.5, 0.5, 0.5, 0.5, 0.5],
    'cardsProcess5': [1, 2, 4, 6, 8],
    'cardsProcess4': [1, 2, 4, 8]
}


class Task:
    def __init__(self, startTime, schedulingTime, createTime, duration, cards):
        self.startTime = startTime
        self.schedulingTime = schedulingTime
        self.createTime = createTime
        self.durationTime = duration
        self.cards = cards
        self.flagTime = None
        self.completeTime = None

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
        self.nodeID = Node.NodeId
        Node.NodeId += 1
        self.cards = cardsPerNode
        self.tasks = []
        self.remainCards = cardsPerNode


class Package:
    def __init__(self, cardsPerPackage: int, nodeId: int):
        self.cards = cardsPerPackage
        self.nodeId = nodeId
        self.task = None

    def __len__(self):
        return self.cards


class Group:
    def __init__(self, cardsPerPackage: int, nodes: Iterable[Node], theta: float):
        self.cardsPerPackage = cardsPerPackage
        self.emptyPackage = []
        self.usedPackage = []
        self.theta = theta
        self.completedTask = []
        self.durationTime = []
        for index, node in enumerate(nodes):
            remainingCards = node.cards
            while remainingCards >= self.cardsPerPackage:
                self.emptyPackage.append(Package(self.cardsPerPackage, node.nodeId))
                remainingCards -= self.cardsPerPackage
                node.remainCards = remainingCards

    def popTask(self, currentTime):
        for index, package in enumerate(self.usedPackage):
            if currentTime - package.task.flagTime >= package.task.durationTime:
                node.remainCards += task.cards
                del node.tasks[index2]
                if node.remainCards == config['cardsPerNode']:
                    del self.usedNodes[index]
                    self.emptyNodes.append(node)
                task.completeTime = currentTime
                self.completed.append(task)
                self.durationTime.append(currentTime - task.createTime)

    def getEmptyNode(self, need):
        assert need == self.cardsProcess
        if next((node for node in self.usedNodes if node.remainCards >= need), None) is not None:
            index = next((index for index, node in enumerate(self.usedNodes) if node.remainCards >= need), None)
            return 1, index
        elif next((node for node in self.emptyNodes if node.remainCards >= need), None) is not None:
            index = next((index for index, node in enumerate(self.emptyNodes) if node.remainCards >= need), None)
            return 2, index
        else:
            return None, None

    def putTask(self, task: Task, currentTime: int):
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


class Groups:
    def __init__(self, cardsPerNode: int, nodeNum: int):
        self.cardsPerNode = cardsPerNode
        self.Gnum = config['GNum']
        self.G = []
        if self.Gnum == 5:
            self.theta = config['theta5']
            self.cardsProcess = config['cardsProcess5']
        elif self.Gnum == 4:
            self.theta = config['theta4']
            self.cardsProcess = config['cardsProcess4']
        avgNum = nodeNum // self.Gnum
        leftNum = nodeNum % self.Gnum
        for i in range(self.Gnum):
            self.G.append(Group(cardsPerNode, avgNum if i != self.Gnum else avgNum + leftNum, self.theta[i],
                                self.cardsProcess[i]))

    def getClass(self, cards):
        if self.Gnum == 5:
            return int(cards // 2)
        elif self.Gnum == 4:
            return int(cards // 2) if cards != 8 else 3

    def up(self, cards):
        '''
        将指定cards的组里的空闲资源整合然后放到别的组里面去
        :param cards:
        :return:
        '''
        index = self.getClass(cards)
