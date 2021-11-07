#-*- coding:utf-8 -*-
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import time

plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False ## 设置正常显示符号
#数据集进行划分，生成点。每三个是一组密度，含糖量
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
#算法模型
def DBSCAN(D, e, Minpts):
  time1=time.perf_counter()
  #初始化核心对象集合T,聚类个数k,聚类集合C, 未访问集合P,
  T = set(); k = 0; C = []; P = set(D)
  for d in D:
    if len([ i for i in D if dist(d, i) <= e]) >= Minpts:
      T.add(d)
  #开始聚类
  while len(T):
    P_old = P
    o = list(T)[np.random.randint(0, len(T))]
    P = P - set(o)
    Q = []; Q.append(o)
    while len(Q):
      q = Q[0]
      Nq = [i for i in D if dist(q, i) <= e]
      if len(Nq) >= Minpts:
        S = P & set(Nq)
        Q += (list(S))
        P = P - S
      Q.remove(q)
    k += 1
    Ck = list(P_old - P)
    T = T - set(Ck)
    C.append(Ck)
  time2=time.perf_counter()
  print('共耗时{:.5f}s'.format(time2 - time1))
  return C
#画图
def draw(C):
  colValue = ['r', 'y', 'g', 'b', 'c', 'k', 'm']
  for i in range(len(C)):
    coo_X = []  #x坐标列表
    coo_Y = []  #y坐标列表
    for j in range(len(C[i])):
      coo_X.append(C[i][j][0])
      coo_Y.append(C[i][j][1])
    plt.scatter(coo_X, coo_Y, marker='o', color=colValue[i%len(colValue)], label=i)
  plt.legend(loc='best')
  plt.title("DBSCAN算法聚类",fontsize=20)
  plt.xlabel("密度")
  plt.ylabel("含糖量")
  plt.show()

if __name__ == '__main__':
    C = DBSCAN(data_split(), 0.11, 6)
    draw(C)