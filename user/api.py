from user.logics import is_phonenum
from user.logics import send_vcode
from libs.http import render_json
from common import errors
from common import keys
from django.core.cache import cache
from user.models import User
from user.forms import  ProfileForm
from user.logics import save_upload_file



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
        '''执行登录注册'''
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
    form = ProfileForm(request.POST)  #通过request.POST 传入所有输入的参数,如果是文件就传入第二个参数
    if form.is_valid():
        '''如果通过post传过来的参数全部有效'''
        profile = form.save(commit=False) #通过调用save方法返回当前model实例
        profile.id = request.user.id
        profile.save()
        return render_json()
    else:
        return render_json(form.errors,code=errors.PROFILE_ERR)  #form.errors把具体的错误传给前端


def upload_avatar(request):
    '''上传个人头像'''
    avatar = request.FILES.get('avatar')
    filename = 'Avatar-%s'% request.user.id
    save_upload_file(filename,avatar)


