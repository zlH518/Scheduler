import pandas as pd

file_path = "./data/tasks_data/mydata1248.csv"


#create_data
random_seed = 3407


#log.py
log_file = './log/info.log'
log_format = "%(asctime)s - %(levelname)s - %(message)s"


#algorithm.py
big_step = 100
step = 1
node_num = 20
cards_per_node = 8
recode_num = 5
experiment_data_path = './experiment'
analysis_path = './experiment/analysis'


#FCFS




#Buddy
group_num = 4
cards_per_group = [1, 2, 4, 8]
theta_per_group = [0.5, 0.5, 0.5, 0.5]
up_time = 5

if __name__ =='__main__':
    data = pd.read_csv(file_path)
    print(data.dtypes)