import os
import re
from random import  randrange
from urllib.parse import urljoin

from common import keys
from libs.qncolud import upload_qncloud
from swiper import config
import requests
from django.core.cache import cache
from django.conf import settings
from worker import celery_app

def is_phonenum(phonenum):
    #检查参数是否是手机号
     pattern = r'(13\d|15[012356789]|166|17[78]|18[01256789]|199)\d{8}$'
     return True if re.match(pattern,phonenum) else False

def gen_rand_code(length=4):
    '''产生验证码'''
    code = randrange(10 ** length)
    #定义一个验证码模板，设置验证码长度为四位%04d,04为限制验证码是4位
    template = '%%0%dd'%length
    return template % code

def send_vcode(phonenum):
    #向第三方平台发送验证码
    vcode = gen_rand_code()
    #将验证码放入缓存，并设置过期时间

    params = config.YZX_SMS_PARAMS.copy()
    params['mobile'] = phonenum
    params['param'] = vcode
    response = requests.post(config.YZX_SMS_API,json=params)
    # print(response.content)
    # print(response.json())
    if response.status_code == 200:
        result = response.json()
        if result.get('msg') == 'OK':
            cache.set(keys.VCODE % phonenum, vcode, 180)
            return True
    return False


def save_upload_file(filename,upload_file):
    '''封装函数，将文件保存到本地服务器'''
    filepath = os.path.join(settings.BASE_DIR,settings.MEDIA_ROOT,filename)
    with open(filepath,'wb') as newfile:
        for chunk in upload_file.chunks():
            newfile.write(chunk)

    return filename,filepath


'''加上celery装饰器，声明此方法需要被django异步调用'''
@celery_app.task
def save_avatar(user,avatar):
    '''异步实现图片的上传'''
    # 定义文件名
    filename = 'Avatar-%s' % user.id

    # 将文件保存到本地服务器
    filename, filepath = save_upload_file(filename, avatar)

    # 将文件上传到云服务器，本地的文件用脚本定期删除掉即可
    upload_qncloud(filename, filepath)

    # 记录头像文件的url
    user.avatar = urljoin(config.QN_HOST, filename)
    user.save()
