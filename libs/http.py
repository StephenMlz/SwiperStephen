import json

from django.http import HttpResponse
from django.conf import settings

def render_json(data=None,code=0):
    result = {
        'data':data,
        'code':code,
    }
    if settings.DEBUG:
        '''括号中间的参数indent是为了在调试模式下更好的显示，sort_keys是为了让key按字母排序'''
        json_str = json.dumps(result,ensure_ascii=False,indent=4,sort_keys=True)
    else:
        json_str = json.dumps(result,ensure_ascii=False,separators=(',',':'))  #此处是为了让返回的json代码更加的紧凑，‘,’和':'之间不会有空格
    return HttpResponse(json_str)

