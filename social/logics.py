from django.core.cache import cache

from common import keys, errors
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





