#系统错误码

OK = 0


class LogicError(Exception):
    '''逻辑错误的基类'''
    code = None
    data = None

    def __init__(self,data=None):
        self.data = data

    def __str__(self):
        return self.__class__.__name__

def gen_logic_err(name,code):
    '''动态创建一个LogicError的子类'''
    bases = (LogicError,)
    attr_dict = {
        'code':code,
    }

    return type(name,bases,attr_dict)


PLATFORM_ERR = gen_logic_err('PLATFORM_ERR ',1000) #第三方平台错误
PHONE_ERR = gen_logic_err('PHONE_ERR ',1001)  #手机号错误
VCODE_ERR = gen_logic_err('VCODE_ERR ',1002) #无效的验证码
LOGIN_REQUIRED = gen_logic_err('LOGIN_REQUIRE ',1003) #用户未登录
PROFILE_ERR = gen_logic_err('PROFILE_ERR ',1004)
USERNOTEXIST = gen_logic_err('USER_DoesNotExist_ERR ',1005) #用户不存在
STYPE_ERR = gen_logic_err('STYPE_ERR ',1006)
REWINDLIMITED = gen_logic_err('RewindLimited ',1007)
PermissonRequired = gen_logic_err('Permission_Err ',1008)