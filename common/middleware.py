import logging

from django.utils.deprecation import MiddlewareMixin
from common import errors
from libs.http import render_json
from user.models import User

err_log = logging.getLogger('err')

class AuthMiddleware(MiddlewareMixin):
    '''设置登录url白名单'''
    WHITE_LIST = [
        '/api/user/get_vcode',
        '/api/user/check_vcode',
    ]

    def process_request(self,request):
        '''如果请求在白名单中，就返回，不执行此中间件,如果请求不在白名单中，则需要进行登录验证'''
        print(request.path)
        if request.path in self.WHITE_LIST:
            return
        #检查用户是否存在，不存在，返回错误码，存在则为request赋予user属性
        uid = request.session.get('uid')
        if not uid:
            err_log.error('%s : %s' % (errors.LOGIN_REQUIRED.code, errors.LOGIN_REQUIRED()))
            return render_json(code=errors.LOGIN_REQUIRED.code)

        else:
            try:
                request.user = User.objects.get(id=uid)
                return
            except User.DoesNotExist:
                err_log.error('%s : %s' % (errors.USERNOTEXIST.code, errors.USERNOTEXIST()))
                return render_json(code=errors.USERNOTEXIST.code)


class LogicMiddleware(MiddlewareMixin):
    #定义异常类中间件：当抛出异常时，异常类中间件先捕获到，并在中间件进行处理

    def process_exception(self,request,exception):
        if isinstance(exception,errors.LogicError):
            data = exception.data or str(exception)  #判断exception 是否是LogicError的实例
            err_log.error('%s : %s' % (exception.code, data))
            return render_json(data=data,code=exception.code)
