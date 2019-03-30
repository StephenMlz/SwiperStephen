from django.shortcuts import render

# Create your views here.
from vip.models import Vip
from libs.http import render_json


def show_vip(request):
    '''VIP和权限展示'''
    vip_info_list = []
    for vip in Vip.objects.all():
        vip_info = vip.to_dict()
        #以字典形式显示vip信息，但perms字段是一个对象，
        # 所以必须再次使之转化为一个字典
        vip_info['perms'] = []
        for perm in vip.perms():
            perm_info = perm.to_dict()
            vip_info['perms'].append(perm_info)
        vip_info_list.append(vip_info)
    return render_json(vip_info_list)

