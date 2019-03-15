from django.db import models
import datetime
from libs.orm import ModelMixin

class User(models.Model):
    SEX = (
        ('male','男性'),
        ('female','女性'),
    )
    LOCATION = (
        ('bj','北京'),
        ('sh','上海'),
        ('gz','广州'),
        ('sz','深圳'),
        ('cd','成都'),
        ('xa','西安'),
        ('wh','武汉'),
        ('zz','郑州'),
        ('nj','南京'),
        ('xm','厦门'),
        ('hz','杭州'),
        ('sy','三亚'),
    )
    phonenum = models.CharField(max_length=16,unique=True,verbose_name='手机号')
    nickname = models.CharField(max_length=32,unique=True,verbose_name='昵称')
    sex = models.CharField(max_length=8,choices=SEX,verbose_name='性别')
    birth_year = models.IntegerField(default=2000,verbose_name='出生年')
    birth_month = models.IntegerField(default=1,verbose_name='出生月')
    birth_day = models.IntegerField(default=1,verbose_name='出生日')
    avatar = models.CharField(max_length=256,verbose_name='个人头像的URL地址')
    location = models.CharField(max_length=16,choices=LOCATION,verbose_name='常居地')

    @property
    def age(self):
        '''用户年龄'''
        today = datetime.date.today()
        birthday = datetime.date(self.birth_year,self.birth_month,self.birth_day,)
        return (today-birthday).days // 365

    def to_dict(self):
        return {
            'phonenum':self.phonenum,
            'nickname':self.nickname,
            'sex':self.sex,
            'age':self.age,
            'avatar':self.avatar,
            'location':self.location,

        }

    @property
    def profile(self):
        '''首先判断，user和profile是一对一的关系，其次为了提高数据库的读写效率，此处省略外键，用给user添加profile属性的方式，让两张表建立联系'''
        if not hasattr(self,'_profile'):
            self._profile, _  = Profile.objects.get_or_create(id=self.id)
        return  self._profile


class Profile(models.Model,ModelMixin):
    '''个人资料'''
    SEX = (
        ('male','男性'),
        ('female','女性'),
    )
    LOCATION = (
        ('bj','北京'),
        ('sh','上海'),
        ('gz','广州'),
        ('sz','深圳'),
        ('cd','成都'),
        ('xa','西安'),
        ('wh','武汉'),
        ('zz','郑州'),
        ('nj','南京'),
        ('xm','厦门'),
        ('hz','杭州'),
        ('sy','三亚'),
    )

    dating_sex = models.CharField(max_length=8,choices=SEX,verbose_name='性别')
    location = models.CharField(max_length=16,choices=LOCATION,verbose_name='常居地')
    min_distance = models.IntegerField(default=1,verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=10,verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18,verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=30,verbose_name='最大交友年龄')
    vibration = models.BooleanField(default=True,verbose_name='是否开启震动')
    only_match = models.BooleanField(default=True,verbose_name='不让未匹配的人查看我的相册')
    auto_play = models.BooleanField(default=True,verbose_name='自动播放视频')