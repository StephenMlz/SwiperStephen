from social import logics
from social.logics import get_rcmd
from libs.http import render_json
from social.models import Swiped
from user.models import User
from vip.logics import need_perm
from social.logics import add_swipe_score
from social.logics import get_top_n


def rcmd_users(request):
    '''获取推荐用户'''
    users = get_rcmd(request.user,10)
    print(users)
    for user in users:
        print(user.id)
    data = [user.to_dict() for user in users]
    return render_json(data=data)

@add_swipe_score
def dislike(request):
    '''左滑，不喜欢'''
    sid = int(request.POST.get('sid'))
    Swiped.swipe(request.user.id,sid,'dislike')
    return render_json()

@add_swipe_score
def like(request):
    '''右滑，喜欢'''
    sid = int(request.POST.get('sid'))
    matched = logics.like_someone(request.user,sid)


    return render_json({'is_matched':matched})


@need_perm('superlike')
@logics.add_swipe_score
def superlike(request):
    '''上滑，超级喜欢'''

    sid = int(request.POST.get('sid'))
    matched = logics.superlike_someone(request.user, sid)

    return render_json({'is_matched': matched})


@need_perm('rewind')
def rewind(request):
    '''反悔'''
    logics.rewind(request.user)

    return render_json()

@need_perm('show_liked_me')
def show_liked_me(request):
    '''查看喜欢我的用户'''
    liked_me_id_list = Swiped.who_liked_me(request.user.id)

    liked_me_users = User.objects.filter(id__in=liked_me_id_list)
    result = [user.to_dict() for user in liked_me_users]

    return render_json(data=result)


def top10(request):
    '''显示排行前10的用户'''
    # 格式: rank_data = {
    #     1: {'id':  3, 'nickname': 'asdf', 'sex': 'male', ..., 'score': 123}
    #     2: {'id':  7, 'nickname': 'bob',  'sex': 'male', ..., 'score': 100}
    #     3: {'id': 15, 'nickname': 'lucy', 'sex': 'female', ..., 'score': 90}
    # }
    rank_data = get_top_n(10)
    return render_json(data=rank_data)
