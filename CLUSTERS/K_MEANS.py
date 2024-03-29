#-*- coding:utf-8 -*-
import numpy as np  # 扩展程序库，针对数组运算提供大量的数学函数库
import pandas as pd  # 加强版numpy，pandas拥有种数据结构：Series和DataFrame
import matplotlib.pyplot as plt  # 绘图库，一种 MatLab 开源替代方案
import random  # 随机数模块
import time  # 时间模块，时间戳时间: float数据类型,给机器用

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False ## 设置正常显示符号
# 西瓜数据集4.0: 密度 含糖率
def  data_split():
    data=pd.read_csv('dataset.txt',encoding='utf-8',names=['密度','含糖量'])
    count= len(data)
    dataset=[]
    for i in range(count):
        a=data.values[i][0]
        b=data.values[i][1]
        dataset.append([a,b])
    return dataset
# 创建类K_means
class K_means(object):
    # 创建__init__方法，在面向对象编程中，给未来创建的对象所定义的进行初始化属性
    # 当对象一旦被创建，Python将会自动调用__init__方法，里面的属性将会赋予这个对象
    def __init__(self, k, data, loop_times, error):  # self只有在类的方法中才会有，指向类的实例对象，而非类本身
        self.k = k
        self.data = data
        self.loop_times = loop_times
        self.error = error

    def distance(self, p1, p2):
        # linalg=linear（线性）+algebra（代数），norm则表示范数
        # 求p = 2 时的闵可夫斯基距离，即欧氏距离
        return np.linalg.norm(np.array(p1) - np.array(p2))

    def fitting(self):
        time1 = time.perf_counter()  # 返回性能计数器的值（以分秒为单位），表示程序开始运行到调用这个语句所经历的时间
        mean_vectors = random.sample(self.data, self.k)  # 随机选取k个初始样本
        initial_main_vectors = mean_vectors
        for vec in mean_vectors :
            plt.scatter(vec[0], vec[1], s=100, color = 'black', marker='s')  # 画出初始聚类中心，以黑色正方形（square）表示

        times = 0
        # map(),高阶函数，它接收一个函数 f 和一个 list，并通过把函数 f 依次作用在 list 的每个元素上，得到一个新的 list 并返回
        # lambda:返回可调用的函数对象，通常是在需要一个函数，但又不想命名一个函数时使用，lambda x : [x] 表示输入x，输出为[x]
        clusters = list(map((lambda x:[x]), mean_vectors))
        while times < self.loop_times:
            change_flag = 1  # 标记簇均值向量是否改变
            for sample in self.data:
                dist = []
                for vec in mean_vectors:
                    dist.append(self.distance(vec, sample))  # 计算样本到每个聚类中心的距离
                clusters[dist.index(min(dist))].append(sample)  # 找到离该样本最近的聚类中心，并将它放入该簇

            new_mean_vectors = []
            for c,v in zip(clusters, mean_vectors):  # zip()将两个对象中对应的元素打包成一个个元组，然后返回由这些元组组成的列表
                cluster_num = len(c)
                cluster_array = np.array(c)
                new_mean_vector = sum(cluster_array) / cluster_num  # 计算出新的聚类簇均值向量
                mean_vector = np.array(v)
                # np.divide和np.true_divide结果一样（python3.7.2）,np.floor_divide只保留整数结果
                # all(iterable):如果iterable(元组或者列表)的所有元素不为0、False或者iterable为空，all(iterable)返回True，否则返回False
                if all(np.true_divide((new_mean_vector - mean_vector), mean_vector) < np.array([self.error, self.error])):
                    new_mean_vectors.append(mean_vector)  # 均值向量未改变
                    change_flag = 0
                else:
                    # dataFrame转List()，括号不能忘
                    new_mean_vectors.append(new_mean_vector.tolist())  # 均值向量发生改变

            if change_flag == 1:
                mean_vectors = new_mean_vectors
            else:
                break
            times += 1
        time2 = time.perf_counter()
        # str.format()，基本语法是通过 {} 和 : 来代替以前的 %
        print ('本次选取的{}个初始向量为{}'.format(self.k, initial_main_vectors))
        print ('共进行{}轮'.format(times))
        print ('共耗时{:.5f}s'.format(time2 - time1))  # 取5位小数
        for cluster in clusters:
            x = list(map(lambda arr: arr[0], cluster))
            y = list(map(lambda arr: arr[1], cluster))
            plt.scatter(x, y, marker = 'o', label = clusters.index(cluster)+1)
        plt.title("K-MEANS算法聚类", fontsize=20)
        plt.xlabel('密度')
        plt.ylabel('含糖率')
        plt.legend(loc='best')
        plt.show()
if __name__ == '__main__':
    for i in [2, 3, 4]:
        # 调用K_means，执行方法fitting()
        k_means = K_means(i, data_split(), 1000, 0.0000001)
        k_means.fitting()

