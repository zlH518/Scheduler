import numpy as np

config = {
    'dataPath': "C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum': 100,
    'cardsPerNode': 8,
    'theat': 0.5,
    'tao': 5
}


class Task:
    def __init__(self, startTime, schedulingTime, createTime, duration, cards):
        self.startTime = startTime
        self.schedulingTime = schedulingTime
        self.createTime = createTime
        self.durationTime = duration
        self.cards = cards
        self.flagTime=None
        self.completeTime=None

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
        self.matrix = np.column_stack((startTime, schedulingTime, createTime, duration, cards))

    def __len__(self):
        return self.matrix.shape[0]


class Node:
    def __init__(self, cardsPerNode: int):
        self.cards = cardsPerNode
        self.tasks = []
        self.remainCards = cardsPerNode

    def __repr__(self):
        return self.cards

class Nodes:
    def __init__(self, nodesNum, cardsPerNode):
        self.emptyNodes = [Node(cardsPerNode) for _ in range(nodesNum)]
        self.usedNodes = []
        self.completed=[]
        self.durationTime=[]

    def cal(self):
        '''
        计算占用率以及碎片率以及act
        :return:
        '''
        pieces=0.0
        for node in self.usedNodes:
            pieces += node.remainCards
        piecesRate = float(pieces/len(self.usedNodes))
        nodeOccupiedRate=float(len(self.usedNodes)/(len(self.usedNodes)+len(self.emptyNodes)))
        act=np.mean(np.array(self.durationTime))
        return {
            'piecesRate':piecesRate,
            'nodeOccupiedRate':nodeOccupiedRate,
            'act':act
        }

    def getEmptyNode(self, need):
        if next((node for node in self.usedNodes if node.remainCards > need), None) is not None:
            self.usedNodes.remove(
                next((index for index, node in enumerate(self.usedNodes) if node.remainCards > need), None))
            return next((node for node in self.usedNodes if node.remainCards > need), None)
        elif next((node for node in self.emptyNodes if node.remainCards > need), None) is not None:
            self.usedNodes.remove(
                next((index for index, node in enumerate(self.usedNodes) if node.remainCards > need), None))
            return next((node for node in self.emptyNodes if node.remainCards > need), None)
        else:
            return None

    def putTask(self, task: Task,currentTime:int):
        '''
        到达一个任务，然后查找空闲且满足条件的node放进去
        :param task:
        :param currentTime:
        :return:
        '''
        node = self.getEmptyNode(task.cards)
        if node is None:
            return False
        task.flagTime = currentTime
        node.remainCards -= task.cards
        node.tasks.append(task)
        self.usedNodes.append(node)
        return True

    def popTask(self, currentTime):
        '''
        将结束的任务从node中释放
        :return:
        '''
        for index,node in enumerate(self.usedNodes):
            for task in node.tasks:
                if currentTime-task.flagTime >= task.durationTime:
                    node.remainCards += task.cards
                    node.tasks.remove(task)
                    if node.remainCards == config['cardsPerNode']:
                        self.usedNodes.remove(index)
                        self.emptyNodes.append(node)
                    task.completeTime = currentTime
                    self.completed.append(task)
                    self.durationTime.append(currentTime-task.createTime)

    def __len__(self):
        return len(self.emptyNodes) + len(self.usedNodes)



