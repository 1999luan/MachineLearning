 #-*- coding:utf-8 -*-
import math
import matplotlib.pyplot as plt
import pandas as pd
import time

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False ## 设置正常显示符号
#数据集进行划分，生成点
def  data_split():
    data=pd.read_csv('dataset.txt',encoding='utf-8',names=['密度','含糖量'])
    count= len(data)
    dataset=[]
    for i in range(count):
        a=data.values[i][0]
        b=data.values[i][1]
        dataset.append((a,b))
    return dataset
#计算欧几里得距离,a,b分别为两个元组
def dist(a, b):
    return math.sqrt(math.pow(a[0]-b[0], 2)+math.pow(a[1]-b[1], 2))

#dist_min
def dist_min(Ci, Cj):
    return min(dist(i, j) for i in Ci for j in Cj)
#dist_max
def dist_max(Ci, Cj):
    return max(dist(i, j) for i in Ci for j in Cj)
#dist_avg
def dist_avg(Ci, Cj):
    return sum(dist(i, j) for i in Ci for j in Cj)/(len(Ci)*len(Cj))

#找到距离最小的下标
def find_Min(M):
    min = 1000
    x = 0; y = 0
    for i in range(len(M)):
        for j in range(len(M[i])):
            if i != j and M[i][j] < min:
                min = M[i][j];x = i; y = j
    return (x, y, min)

#算法模型：
def AGNES(dataset, dist, k):
    time1=time.perf_counter()
    #初始化C和M
    C = [];M = []
    for i in dataset:
        Ci = []
        Ci.append(i)
        C.append(Ci)
    for i in C:
        Mi = []
        for j in C:
            Mi.append(dist(i, j))#Mi中存放了i簇到其余簇的距离
        M.append(Mi) #保存了两簇之间的距离
    q = len(dataset)
    #合并更新
    while q > k:
        x, y, min = find_Min(M)
        C[x].extend(C[y])#两个簇进行合并
        C.remove(C[y])#从全部簇的列表中删除被合并的簇
        #更新簇之间的距离
        M = []
        for i in C:
            Mi = []
            for j in C:
                Mi.append(dist(i, j))
            M.append(Mi)
        q -= 1
    time2=time.perf_counter()
    print('共耗时{:.5f}s'.format(time2 - time1))
    return C
#画图
def draw(C):
    colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
    for i in range(len(C)):
        coo_X = []    #x坐标列表
        coo_Y = []    #y坐标列表
        for j in range(len(C[i])):
            coo_X.append(C[i][j][0])
            coo_Y.append(C[i][j][1])
        plt.scatter(coo_X, coo_Y, marker='o', color=colValue[i%len(colValue)], label=i)
    plt.legend(loc='best')
    plt.title("AGNES算法聚类", fontsize=20)
    plt.xlabel("密度")
    plt.ylabel("含糖量")
    plt.show()
if __name__ == '__main__':
    C = AGNES(data_split(), dist_max, 2)
    draw(C)
