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

config={
    'dataPath':"C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum':6000,
    'cardsPerNode':8,
    'theat':0.5,
    'tao':5
}
