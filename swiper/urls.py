
from django.conf.urls import url
from user import api as user_api
from social import api as social_api
from vip import api as vip_api

urlpatterns = [
    url(r'api/user/get_vcode',user_api.get_vcode),      #获取验证码 phonenum
    url(r'api/user/check_vcode',user_api.check_vcode),  #校验验证码 phonenum vcode nickname
    url(r'api/user/get_profile',user_api.get_profile),  #查看交友需求
    url(r'api/user/set_profile',user_api.set_profile),  #设置交友需求   'dating_sex','location','min_distance','max_distance','min_dating_age','max_dating_age',
    url(r'api/user/upload_avatar',user_api.upload_avatar),#上传个人头像   avatar
    url(r'api/social/rcmd_users',social_api.rcmd_users),  #查看推荐用户

    url(r'api/social/like',social_api.like),   #喜欢  sid
    url(r'api/social/dislike',social_api.dislike),  #不喜欢  sid
    url(r'api/social/superlike',social_api.superlike),#超级喜欢  sid
    url(r'api/social/rewind',social_api.rewind),    #反悔（解除好友关系）
    url(r'api/social/show_liked_me',social_api.show_liked_me),#查看谁喜欢我

    url(r'api/social/top10',social_api.top10),#查看Top10
    url(r'api/vip/show_vip',vip_api.show_vip),#查看vip权限
]
