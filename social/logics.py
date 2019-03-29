from django.core.cache import cache

from common import keys, errors
from libs.cache import rds
from social.models import Swiped
from swiper import config
from user.models import User
import datetime,time
from social.models import Friend

def get_rcmd(user,limit):
    '''为user用户推荐称心的用户'''

    #筛选出user用户已经滑动过的用户
    # user_swiped = Swiped.objects.filter(uid=user.id).only('sid')
    # swiped_sid_list = [swiped.sid for swiped in user_swiped]
    swiped_sid_list = Swiped.objects.filter(uid=user.id).values_list('sid',flat=True)

    #根据user用户如意的年龄范围，算出出生年份区间，以便查找
    today = datetime.date.today()
    min_year = today.year - user.profile.max_dating_age
    max_year = today.year - user.profile.min_dating_age

    #筛选出user用户如意的用户，并返回
    rcmd_users = User.objects.filter(sex=user.profile.dating_sex,
                        location=user.profile.location,
                        birth_year__gte=min_year,
                        birth_year__lte=max_year
                        ).exclude(id__in=swiped_sid_list)[:limit]
    return rcmd_users


def like_someone(user,sid):
    '''添加一条喜欢的滑动记录'''
    Swiped.swipe(user.id,sid,'like')

    #检查对方是否喜欢过自己,如果喜欢过，两者建立好友关系
    if Swiped.is_liked(sid,user.id):
        Friend.make_friends(user.id,sid)
        return True
    else:
        return False


def superlike_someone(user,sid):
    '''添加一条喜欢的滑动记录'''
    Swiped.swipe(user.id, sid, 'superlike')

    # 检查对方是否喜欢过自己,如果喜欢过，两者建立好友关系
    if Swiped.is_liked(sid, user.id):
        Friend.make_friends(user.id, sid)
        return True
    else:
        return False

def rewind(user):
    '''反悔'''
    key = keys.REWIND_TIMES % user.id

    rewind_times= cache.get(key,0)
    if rewind_times >= config.REWIND_LIMIT:
        raise  errors.REWINDLIMITED



    #找出当前用户最后一条滑动记录
    latest_swiped = Swiped.objects.filter(uid=user.id).latest('stime')

    #检查之前是好友，如果是好友则断交
    if latest_swiped.flag in ['like','superlike']:

        #有则删除，无则什么都不做
        Friend.break_off(user.id,latest_swiped.sid)
    #删除滑动记录
    latest_swiped.delete()

    rewind_times += 1

    #设置过期时间：当天晚上12点过期，time.time()当前时间戳，
    remain_time = 86400 - (time.time() + 3600 * 8 ) % 86400
    cache.set(key,rewind_times,remain_time)

    #设置过期时间的另一种方法

    # now_time = datetime.datetime.now().time()
    # remain_time = 86400 - now_time.hour * 3600 - now_time.minute * 60 - now_time.second
    # cache.set(key, rewind_times, remain_time)


def add_swipe_score(swipe_view_func):
    def wrapper(request):
        response = swipe_view_func(request)

        if 200 <= response.status_code < 300:
            # 记录被滑动用户的积分
            stype = swipe_view_func.__name__
            score = config.SWIPE_SCORE[stype]
            sid = request.POST.get('sid')
            rds.zincrby(keys.SWIPE_RANK, score, sid)

        return response
    return wrapper


def get_top_n(num):
    '''获取排行前 N 的用户数据'''
    # 数据格式
    # origin_data = [
    #     (b'575', 920.0),  # 第一项是 uid, 第二项是"用户积分"
    #     (b'778', 624.0),
    #     (b'632', 520.0),
    # ]
    origin_data = rds.zrevrange(keys.SWIPE_RANK,0,num-1,withscores=True)
    print(origin_data)

    #整理数据格式
    cleaned_data= [[int(uid),int(score)] for uid,score in origin_data]

    rank_data = {}
    for rank,(uid,score) in enumerate(cleaned_data,1):
        user = User.get(id=uid) #Note:此处可以改成批量获取，提升数据操作性能
        user_data = user.to_dict()
        user_data['score'] = score
        rank_data[rank] = user_data
    return rank_data

