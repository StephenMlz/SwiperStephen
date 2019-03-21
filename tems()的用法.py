
x = {
    'name':'stephen',
    'age':27,
}
for key,value in x.items():
    print(x.items())
    print(key,value)

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

# l = []
# for i in range(10):
#     l.append({
#         'num':i
#     })
# print(l)
#
#
# l2 = []
# a = {'num':0}
# for i in range(10):
#     a['num'] = i
#     l2.append(a)
# print(l2)
#
# '''
# [{'num': 0}, {'num': 1}, {'num': 2}, {'num': 3}, {'num': 4}, {'num': 5}, {'num': 6}, {'num': 7}, {'num': 8}, {'num': 9}]
# [{'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}, {'num': 9}]
class A(object):
    instance = None
    def new(cls,*args,**kwargs):
        if cls. instance is None:
            cls.instance = object. new (cls)
            return cls.instance
        else:
            return cls.instance
# 1.2 单例模式的应用场景有哪些？(2018-4-16-lxy)
#
# 单例模式应用的场景一般发现在以下条件下：
# （1）资源共享的情况下，避免由于资源操作时导致的性能或损耗等。如日志文件，应用配置。
# （2）控制资源的情况下，方便资源之间的互相通信。如线程池等。
# 1.网站的计数器
# 2.应用配置
# 3.多线程池
# 4. 数据库配置，数据库连接池
# 5.应用程序的日志应用....





