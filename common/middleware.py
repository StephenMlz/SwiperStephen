from django.utils.deprecation import MiddlewareMixin
from common import errors
from libs.http import render_json
from user.models import User
from django.http import HttpResponse

class AuthMiddleware(MiddlewareMixin):
    '''设置登录url白名单'''
    WHITE_LIST = [
        '/api/user/submit_phone',
        '/api/user/submit_vcode',
    ]

    def process_request(self,request):
        '''如果请求在白名单中，就返回，不执行此中间件,如果请求不在白名单中，则需要进行登录验证'''
        print(request.path)
        if request.path in self.WHITE_LIST:
            return
        #检查用户是否存在，不存在，返回错误码，存在则给request赋予user属性
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRE)

        else:
            try:
                request.user = User.objects.get(id=uid)
            except User.DoesNotExist:
                return render_json(code=errors.USER_DoesNotExist_ERR)