from common.errors import PermissonRequired

'''VIP权限检查装饰器,另外写的一个简单装饰器'''
def dec(func):
    def wrapper(request):
        user = request.user
        print(user.id)
        print(user.vip_id)

        vip_id = user.vip_id

        if func.__name__ == 'superlike' and vip_id in [2,3,4]:
            return func(request)
        elif func.__name__ == 'rewind' and vip_id in [3,4]:
            return func(request)
        elif func.__name__ == 'show_liked_me' and vip_id == 4:
            return func(request)
        else:
            raise PermissonRequired


    return wrapper