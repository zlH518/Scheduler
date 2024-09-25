#dataprepare.py
file_path = "C:\\Users\\Administrator\\Desktop\\IdsLab\\任务\\SchedulerSystem\\Code\\version1\\data\\testForBuddy.csv"


#log.py
log_file = 'C:\\Users\\Administrator\\Desktop\\IdsLab\\任务\\SchedulerSystem\\Code\\version1\\experiment_data\\Test\\log\\info.log'
log_format = "%(asctime)s - %(levelname)s - %(message)s"


#algorithm.py
big_step = 100
step = 100
node_num = 5
cards_per_node = 8
recode_num = 5
experiment_data_path = 'C:\\Users\\Administrator\\Desktop\\IdsLab\\任务\\SchedulerSystem\\Code\\version1\\experiment_data\\Test'
analysis_path = 'C:\\Users\\Administrator\\Desktop\\IdsLab\\任务\\SchedulerSystem\\Code\\version1\\experiment_data\\Test'


#FCFS

#Buddy
group_num = 5
cards_per_group = [1, 2, 4, 6, 8]
theta_per_group = [0.5, 0.5, 0.5, 0.5, 0.5]
up_time = 200
