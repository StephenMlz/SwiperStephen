from user.logics import is_phonenum
from user.logics import send_vcode
from libs.http import render_json
from common import errors

def submit_phone(request):
    #提交手机号，发送验证码
    phonenum = request.POST.get('phonenum')
    if is_phonenum(phonenum):
        #生成验证码
        #向短信平台发送验证码
        if send_vcode(phonenum):
            return render_json(None)
        else:
            return render_json(None,errors.PLATFORM_ERR)

    else:
        return render_json({'error':errors.PHONE_ERR})

def submit_vcode(request):

    pass

