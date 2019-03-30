from user.logics import is_phonenum, save_avatar
from user.logics import send_vcode
from libs.http import render_json
from common import errors
from common import keys
from django.core.cache import cache
from user.models import User
from user.forms import  ProfileForm


def get_vcode(request):
    #提交手机号，发送验证码
    phonenum = request.POST.get('phonenum')
    if is_phonenum(phonenum):
        #生成验证码
        #向短信平台发送验证码
        if send_vcode(phonenum):
            print(phonenum)
            return render_json()
        else:
            raise errors.PLATFORM_ERR

    else:
        raise errors.PHONE_ERR()

def check_vcode(request):
    '''从缓存取出验证码，并与输入的验证码进行验证，验证成功，进行注册或登录'''
    phone = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    nickname = request.POST.get('nickname')

    cached_vcode = cache.get(keys.VCODE % phone)
    if vcode == cached_vcode:
        '''执行登录注册'''
        try:
            user = User.objects.get(phonenum=phone)
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phone,nickname=nickname)

        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        raise errors.VCODE_ERR

def get_profile(request):
    '''获取个人资料'''
    key = keys.PROFILE % request.user.id
    profile_dict = cache.get(key)
    print('从缓存获取%s'%profile_dict)
    if profile_dict is None:  #is  比 == 更精确
        profile_dict = request.user.profile.to_dict()
        print('从数据库获取%s' % profile_dict)
        cache.set(key,profile_dict,3600)
        print('写入缓存')
    return render_json(data=profile_dict)


def set_profile(request):
    '''修改个人资料'''
    form = ProfileForm(request.POST)  #通过request.POST 传入所有输入的参数,如果是文件就传入第二个参数
    if form.is_valid():
        '''如果通过post传过来的参数全部有效'''
        profile = form.save(commit=False) #通过调用save方法返回当前model实例
        profile.id = request.user.id
        profile.save()

        #修改缓存
        key = keys.PROFILE % request.user.id
        cache.set(key, profile.to_dict(), 3600)
        print('修改缓存')
        return render_json()
    else:
        raise errors.PROFILE_ERR(form.errors)  #form.errors把具体的错误传给前端


def upload_avatar(request):
    '''上传个人头像,先保存到本地，再上传到七牛云服务器'''
    user = request.user
    #获取文件
    avatar = request.FILES.get('avatar')
    #celery异步调用，实现文件快速上传
    save_avatar.delay(user, avatar)

    return render_json()








