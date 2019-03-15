'''
 -*- coding: utf-8 -*-
 @Time : 19-3-14 下午2:11
 @Author : SamSa
 @Site : 
 @File : tems()的用法.py
 @Software: PyCharm
'''
# x = {
#     'name':'stephen',
#     'age':27
# }
# for key,value in x.items():
#     print(key,value)

# n = (lambda  x,y:x + y)(1,5)
# print(n)
# n = (lambda  x,y=0,z=0:x+y+z)(1,5,6)
# print(n)

# from random import randrange
#
# length = 4
# code = randrange(10 ** length)
# print(code)
# template = '%%0%dd' %   length
# print(template)
# print(template % code )

l = []
for i in range(10):
    l.append({
        'num':i
    })
print(l)


l2 = []
a = {'num':0}
for i in range(10):
    a['num'] = i
    l2.append(a)
print(l2)

'''
[{'num': 0}, {'num': 1}, {'num': 2}, {'num': 3}, {'num': 4}, {'num': 5}, {'num': 6}, {'num': 7}, {'num': 8}, {'num': 9}]
[{'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}]
'''

