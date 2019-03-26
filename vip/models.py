from django.db import models

# Create your models here.
from libs.orm import ModelMixin


class Vip(models.Model,ModelMixin):
    '''会员表'''
    name = models.CharField(max_length=16,verbose_name='VIP名称',unique=True)
    level = models.IntegerField(verbose_name='会员等级')
    price = models.FloatField(verbose_name='会员价格')

    def perms(self):
        pid_id_list = VipPermRalation.objects.filter(vid=self.id)\
            .values_list('pid',flat=True)
        perm_list = Permission.objects.filter(id__in=pid_id_list)
        return perm_list
    def has_perm(self,perm_name):
        '''检查是够具有某种权限'''
        for perm in self.perms():
            if perm.name == perm_name:
                return True
        return False


class Permission(models.Model,ModelMixin):
    '''权限表'''
    name = models.CharField(max_length=10,verbose_name='权限名称'
                            ,unique=True)
    description = models.TextField(verbose_name='权限详情介绍')


class VipPermRalation(models.Model):
    '''会员权限关系表'''
    vid = models.IntegerField(verbose_name='会员的ID')
    pid = models.IntegerField(verbose_name='权限的ID')


