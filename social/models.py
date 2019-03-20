from django.db import models


class Swiped(models.Model):
    FLAGS = (
        ('like','喜欢'),
        ('superlike','超级喜欢'),
        ('dislike','不喜欢')
    )
    uid = models.IntegerField(verbose_name='滑动者的uid')
    sid = models.IntegerField(verbose_name='被滑动者的sid')
    flag = models.CharField(max_length=16,choices=FLAGS,verbose_name='滑动类型')
    time = models.DateTimeField(auto_now_add=True,verbose_name='滑动时间')