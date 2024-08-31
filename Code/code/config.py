import numpy as np
import pandas as pd

import random

class Task:
    def __init__(self, startTime,schedulingTime,createTime,duration,cards):
        self.startTime = startTime
        self.schedulingTime=schedulingTime
        self.createTime=createTime
        self.durationTime=duration
        self.cards=cards

    def __repr__(self):
        return (f"Task(createTime:{self.createTime}, startTime={self.startTime}, "
                f"end_time={self.endTime}, schedulingTime:{self.schedulingTime},"
                f"durationTime:{self.durationTime}, cards:{self.cards})\n")


config={
    'dataPath':"C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\data/*.json",
    'nodeNum':6000,
    'cardsPerNode':8,
    'theat':0.5,
    'tao':5
}
