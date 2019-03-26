from django.db import models
from common import errors
from django.db.models import Q

class Swiped(models.Model):
    FLAGS = (
        ('dislike','左滑'),
        ('superlike','上滑'),
        ('like','右滑')
    )
    uid = models.IntegerField(verbose_name='滑动者的uid')
    sid = models.IntegerField(verbose_name='被滑动者的sid')
    flag = models.CharField(max_length=16,choices=FLAGS,verbose_name='滑动类型')
    stime = models.DateTimeField(auto_now_add=True,verbose_name='滑动时间')

    @classmethod
    def swipe(cls,uid,sid,stype):
        '''为用户添加滑动记录'''
        #考虑滑动错误操作的情况
        if stype not in ['dislike','superlike','like']:
            raise errors.STYPE_ERR

        #使用get_or_create来避免重复创建滑动记录
        swiped, _ =  cls.get_or_create(uid=uid,sid=sid,flag=stype)

        return swiped,False

    @classmethod
    def is_liked(cls,uid,sid):
        '''检查是否喜欢过某人'''
        return cls.objects.filter(uid=uid,sid=sid,flag__in=['like','superlike']).exists()


    @classmethod
    def who_liked_me(cls,uid):
        '''喜欢过我的人的ID'''
        liked_me = cls.objects.filter(sid=uid,flag__in=['like','superlike'])
        liked_me_id_list = liked_me.values_list('uid',flat=True)
        return liked_me_id_list


class Friend(models.Model):
    uid1 = models.IntegerField(verbose_name='好友1的ID')
    uid2 = models.IntegerField(verbose_name='好友2的ID')

    @classmethod
    def make_friends(cls,uid1,uid2):
        '''建立好友关系'''
        #好友id不分顺序，自动排序,但要确定一条好友关系，是唯一的，所以要为ID排序
        uid1,uid2 = (uid2,uid1) if uid1 > uid2 else (uid1,uid2)

        friends, _ = cls.get_or_create(uid1=uid1,uid2=uid2)

        return friends,False

    @classmethod
    def break_off(cls,uid1,uid2):
        '''断交'''
        uid1,uid2 = (uid2,uid1) if uid1 > uid2 else (uid1,uid2)

        cls.objects.filter(uid1=uid1,uid2=uid2).delete()

    @classmethod
    def is_friends(cls,uid1,uid2):
        '''检查将个人是否是好友关系'''
        uid1,uid2 = (uid2,uid1) if uid1 > uid2 else (uid2,uid1)

        return cls.objects.filter(uid1=uid1,uid2=uid2).exists()

    @classmethod
    def friends_id_list(cls,uid):
        '''获取所有好友的ID'''

        condition = Q(uid1=uid) | Q(uid2=uid)
        all_friends = cls.objects.filter(condition)

        fid_list = []

        for friends in all_friends:

            fid = friends.uid1 if friends.uid2==uid else friends.uid2
            fid_list.append(fid)

        return fid_list





