from Buddy import mywork
from FCFS import FCFS
import matplotlib.pyplot as plt
from B1 import Work
from B2 import Work2
import numpy as np
import seaborn as sns
cmp = sns.color_palette("tab10")

time1,act1=mywork()
time2,act2=FCFS()
time3,act3=Work(time1,act1,time2)
time4,act4=Work2(time1,act1,time2)
plt.figure(figsize=(10, 5))
plt.plot(time1, act1, label='mywork', color=cmp[0])
plt.plot(time2, act2, label='FCFS', color=cmp[1])
plt.plot(time3, act3, label='B1', color=cmp[2])
plt.plot(time4, act4, label='B2', color=cmp[3])
plt.title('Act')
plt.xlabel('Time')
plt.ylabel('Act')
plt.grid(True)
plt.savefig('C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\img\compare4.png')
plt.show()