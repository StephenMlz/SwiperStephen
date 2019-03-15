from django.utils.deprecation import MiddlewareMixin
from common import errors
from libs.http import render_json

class AuthMiddleware(MiddlewareMixin):
    '''设置登录url白名单'''
    WHITE_LIST = [
        'api/user/submit_phone',
        'api/user/submit_vcode',
    ]

    def process_request(self,request):
        '''如果请求在白名单中，就返回，不执行此中间件'''
        if request.path in self.WHITE_LIST:
            return
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRE)

