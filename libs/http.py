import json

from django.http import HttpResponse

def render_json(data,code=0):
    result = {
        'data':data,
        'code':code,
    }
    json_str = json.dumps(result,separators=(',',':'))  #此处是为了让返回的json代码更加的紧凑，‘,’和':'之间不会有空格
    return HttpResponse(json_str)

