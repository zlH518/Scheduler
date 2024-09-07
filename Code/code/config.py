import numpy as np

config = {
    'dataPath': "C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum': 50,
    'cardsPerNode': 8,
    'tao': 5,
    'GNum': 5,
    'theta4':[0.5,0.5,0.5,0.5],
    'theta5':[0.5,0.5,0.5,0.5,0.5],
    'cardsProcess5':[1,2,4,6,8],
    'cardsProcess4':[1,2,4,8]
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
        self.completed = []
        self.durationTime = []

    def cal(self):
        '''
        计算占用率以及碎片率以及act
        :return:
        '''
        pieces = 0.0
        for node in self.usedNodes:
            pieces += node.remainCards
        piecesRate = float(pieces / len(self.usedNodes)) if len(self.usedNodes) != 0 else 0.0
        nodeOccupiedRate = float(len(self.usedNodes) / (len(self.usedNodes) + len(self.emptyNodes)))
        act = np.mean(np.array(self.durationTime))
        return {
            'piecesRate': piecesRate,
            'nodeOccupiedRate': nodeOccupiedRate,
            'act': act,
            'emptycards': len(self.emptyNodes)
        }

    def getEmptyNode(self, need):
        if next((node for node in self.usedNodes if node.remainCards >= need), None) is not None:
            index = next((index for index, node in enumerate(self.usedNodes) if node.remainCards >= need), None)
            return 1, index
        elif next((node for node in self.emptyNodes if node.remainCards >= need), None) is not None:
            index = next((index for index, node in enumerate(self.emptyNodes) if node.remainCards >= need), None)
            return 2, index
        else:
            return None, None

    def putTask(self, task: Task, currentTime: int):
        '''
        到达一个任务，然后查找空闲且满足条件的node放进去
        :param task:
        :param currentTime:
        :return:
        '''
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

    def popTask(self, currentTime):
        '''
        将结束的任务从node中释放
        :return:
        '''
        for index, node in enumerate(self.usedNodes):
            for index2, task in enumerate(node.tasks):
                if currentTime - task.flagTime >= task.durationTime:
                    node.remainCards += task.cards
                    del node.tasks[index2]
                    if node.remainCards == config['cardsPerNode']:
                        del self.usedNodes[index]
                        self.emptyNodes.append(node)
                    task.completeTime = currentTime
                    self.completed.append(task)
                    self.durationTime.append(currentTime - task.createTime)

    def __len__(self):
        return len(self.emptyNodes) + len(self.usedNodes)

    def isEmpty(self):
        if len(self.usedNodes) == 0:
            return True
        else:
            return False


class Group:
    def __init__(self, cardsPerNode, nodeNum, theta, cardsProcess):
        self.cardsPerNode = cardsPerNode
        self.emptyNodes = [Node(cardsPerNode) for _ in range(nodeNum)]
        self.usedNodes = []
        self.theta = theta
        self.completed = []
        self.durationTime = []
        self.cardsProcess=cardsProcess

    def popTask(self,currentTime):
        for index, node in enumerate(self.usedNodes):
            for index2, task in enumerate(node.tasks):
                if currentTime - task.flagTime >= task.durationTime:
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
        self.G=[]
        if self.Gnum == 5:
            self.theta = config['theta5']
            self.cardsProcess=config['cardsProcess5']
        elif self.Gnum == 4:
            self.theta = config['theta4']
            self.cardsProcess=config['cardsProcess4']
        for i in range(self.Gnum):
            self.G.append(Group(cardsPerNode, nodeNum, self.theta[i], self.cardsProcess[i]))

    def getClass(self, cards):
        if self.Gnum == 5:
            return self.G[int(cards // 2)]
        elif self.Gnum == 4:
            return self.G[int(cards // 2)] if cards != 8 else self.G[4]

    def

