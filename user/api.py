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
    phone = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')
    nickname = request.POST.get('nickname')
    cached_vcode = cache.get(keys.VCODE % phone)
    if vcode == cached_vcode:
        user, _ = User.objects.get_or_create(phonenum=phone,nickname=nickname)
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        return render_json(code=errors.VCODE_ERR)



