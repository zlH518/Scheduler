import numpy as np


def generate_random_data(data1, data2, percentage):

    # 生成随机数据
    random_data = np.array(data1*0.7) + np.random.uniform(-offsets, offsets, size=length)

    return random_data
