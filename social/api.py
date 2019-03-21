
from social.logic import rcmd
from libs.http import render_json

def rcmd_users(request):
    '''获取已登录用户的推荐用户，并将推荐用户的资料返回页面'''
    users = rcmd(request.user)
    print(users)
    data = [user.to_dict() for user in users]
    return render_json(data=data)


def like(request):
    return render_json()

def superlike(request):
    return render_json()

def dislike(request):
    return render_json()

def rewind(request):
    return render_json()

def show_liked_me(request):
    return render_json()
