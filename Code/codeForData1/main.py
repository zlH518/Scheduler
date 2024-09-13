from Buddy import mywork
from FCFS import FCFS
import matplotlib.pyplot as plt

time1,act1=mywork()
time2,act2=FCFS()
plt.figure(figsize=(10, 5))
plt.plot(time1, act1, label='mywork', color='green')
plt.plot(time2, act2, label='FCFS', color='red')
plt.title('Act')
plt.xlabel('Time')
plt.ylabel('Act')
plt.grid(True)
plt.savefig('C:\\Users\Administrator\Desktop\IdsLab\任务\SchedulerSystem\Code\img\compare3.png')
plt.show()