#!/usr/bin/python
# -*- coding: UTF-8 -*-


'''
    创建二分法查找函数，假设L是一个有序列表，x是要查找的元素,
    如果在L中找到x，则返回x这个元素在L中的索引，否则返回‘x不存在’的信息
'''
# 定义m为位移，起始值是0
m = 0

def find2(x,L):
    global m
    n = int(len(L)/2)
    # 如果列表只有一个元素且x与之不相等：
    if n == 0 and x != L[0]:
        print('x is not here!')
    # 如果列表只有一个元素且x与之相等：
    elif n ==0 and x == L[0]:
        print('x=L[%d]' %(m))
    # 如果列表元素有两个及以上，且x小于中间元素，只需截取列表前一半：
    elif x < L[n]:
        find2(x,L[:n])
    # 如果列表元素有两个及以上，且x大于中间元素，只需截取列表后一半：
    elif x > L[n]:
        # 起始位移不再是m，而是m+n：
        m = m + n
        find2(x,L[n:])
    # 如果x等于中间元素，直接打印结果：
    else:
        print('x=L[%d]' %(m+n))

List = range(1)
find2(5,List)
