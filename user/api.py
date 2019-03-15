from user.logics import is_phonenum
from user.logics import send_vcode
from libs.http import render_json
from common import errors
from common import keys
from django.core.cache import cache
from user.models import User



def submit_phone(request):
    #提交手机号，发送验证码
    phonenum = request.POST.get('phonenum')
    if is_phonenum(phonenum):
        #生成验证码
        #向短信平台发送验证码
        if send_vcode(phonenum):
            print(phonenum)
            return render_json()
        else:
            return render_json(code=errors.PLATFORM_ERR)

    else:
        return render_json(code=errors.PHONE_ERR)

def submit_vcode(request):
    '''从缓存取出验证码，并与输入的验证码进行验证，验证成功，进行注册或登录'''
    phone = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    nickname = request.POST.get('nickname')
    cached_vcode = cache.get(keys.VCODE % phone)
    if vcode == cached_vcode:
        '''执行登录，注册'''
        user, _ = User.objects.get_or_create(phonenum=phone,nickname=nickname)
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERR)

def get_profile(request):
    '''获取个人资料'''
    user = request.user
    return render_json(data=user.profile.to_dict('vibration','only_match','auto_play'))
def set_profile(request):
    '''修改个人资料'''
    user = request.user
    pass
def upload_avatar(request):
    '''上传个人头像'''
    user = request.user
    pass

