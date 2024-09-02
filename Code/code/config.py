import numpy as np

class Task:
    def __init__(self, startTime,schedulingTime,createTime,duration,cards):
        self.startTime = startTime
        self.schedulingTime=schedulingTime
        self.createTime=createTime
        self.durationTime=duration
        self.cards=cards

    def __repr__(self):
        return (f"Task(createTime:{self.createTime}, startTime={self.startTime}, "
                f"schedulingTime:{self.schedulingTime},durationTime:{self.durationTime}, "
                f"cards:{self.cards})\n")

class ALLTasks:
    def __init__(self,index:list,data:list):
        self.index=index
        self.allTask=data
        startTime = np.array([task.startTime for task in data])
        schedulingTime = np.array([task.schedulingTime for task in data])
        createTime = np.array([task.createTime for task in data])
        duration = np.array([task.durationTime for task in data])
        cards = np.array([task.cards for task in data])
        self.matrix=np.column_stack((startTime,schedulingTime,createTime,duration,cards))

    def __len__(self):
        return self.matrix.shape[0]

class Node:
    def __init__(self,cardsPerNode:int):
        self.cards=cardsPerNode
        self.tasks=[]
        self.remainCards=cardsPerNode

class Nodes:
    def __init__(self,nodesNum,cardsPerNode):
        self.nodes=[Node(cardsPerNode) for _ in range(nodesNum)]
        self.cards=np.array([cardsPerNode for _ in range(nodesNum)],dtype=np.int)

    def calUtilization(self):
        pass

    def getEmptyNode(self,need):
        return np.where(self.cards>need)[0]

    def putTask(self,idx,task:Task):
        self.nodes[idx].tasks.append(task)
        self.nodes[idx].remainCards-=task.cards
        self.cards[idx]
    def __len__(self):
        return len(self.nodes)




config={
    'dataPath':"C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum':100,
    'cardsPerNode':8,
    'theat':0.5,
    'tao':5
}
