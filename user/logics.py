'''
 -*- coding: utf-8 -*-
 @Time : 19-3-14 下午1:05
 @Author : SamSa
 @Site : 
 @File : logics.py.py
 @Software: PyCharm
'''
import re
from random import  randrange

from swiper import config
import requests

def is_phonenum(phonenum):
    #检查参数是否是手机号
     pattern = r'(13\d|15[012356789]|166|17[78]|18[0126789]|199)\d{8}$'
     return True if re.match(pattern,phonenum) else False

def gen_rand_code(length=4):
    '''产生验证码'''
    code = randrange(10 ** length)
    #定义一个验证码模板，设置验证码长度为四位%04d,04为限制验证码是4位
    template = '%%0%dd'%length
    return template % code

def send_vcode(phonenum):
    #向第三方平台发送验证码
    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phonenum
    params['param'] = gen_rand_code()
    response = requests.post(config.YZX_SMS_API,json=params)
    if response.status_code == 200:
        result = response.json()
        if result.get('msg') == 'ok':
            return True
    return False

