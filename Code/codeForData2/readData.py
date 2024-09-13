import csv

# 定义一个空列表来存储Task实例
data = []

# 打开CSV文件
with open('trace_seren.csv', 'r') as csvfile:
    # 创建CSV阅读器
    csvreader = csv.DictReader(csvfile)

    # 遍历CSV文件中的每一行
    for row in csvreader:
        # 检查node_num是否为1
        if row['node_num'] == '1':
            # 创建Task实例并添加到data列表中
            task = Task(
                job_id=row['job_id'],
                user=row['user'],
                node_num=int(row['node_num']),
                gpu_num=int(row['gpu_num']),
                cpu_num=int(row['cpu_num']),
                type=row['type'],
                state=row['state'],
                submit_time=row['submit_time'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                duration=int(row['duration']),
                queue=int(row['queue']),
                gpu_time=float(row['gpu_time'])
            )
            data.append(task)

# 现在data列表中包含了所有node_num为1的Task实例