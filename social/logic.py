from social.models import Swiped
from user.models import User
import datetime


def rcmd(user):
    '''为user用户推荐称心的用户'''

    #筛选出user用户已经滑动过的用户
    user_swiped = Swiped.objects.filter(uid=user.id).only('sid')
    swiped_sid_list = [swiped.sid for swiped in user_swiped]

    #根据user用户如意的年龄范围，算出出生年份区间，以便查找
    today = datetime.date.today()
    min_year = today.year - user.profile.max_dating_age
    max_year = today.year - user.profile.min_dating_age

    #筛选出user用户如意的用户，并返回
    users = User.objects.filter(sex=user.profile.dating_sex,
                        location=user.profile.location,
                        birth_year__gte=min_year,
                        birth_year__lte=max_year
                        ).exclude(id__in=swiped_sid_list)
    return users