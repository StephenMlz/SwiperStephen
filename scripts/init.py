# !/usr/bin/env python

'''脚本文件夹是一个独立的文件夹，它不能被其他模块调用,如果shell调用，要配置环境'''
import os
import sys
import random
import django

#设置环境
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "swiper.settings")
django.setup()

from django.db.utils import IntegrityError

from user.models import User

last_names = (

    '赵钱孙李周吴郑王冯陈褚卫蒋沈韩杨朱秦尤许何吕施张孔曹严华金魏陶姜'
    '戚谢邹喻柏水窦章云苏潘葛奚范彭郎鲁韦昌马苗凤花方俞任袁柳鲍史唐'
    '费廉岑薛雷贺倪汤滕殷罗毕郝安常乐于时傅皮卞齐康伍余元卜顾孟平黄'
    '程穆萧尹姚邵湛汪祁毛禹狄米贝明臧计伏成戴谈宋茅庞熊纪舒屈项祝董梁'
    '杜阮蓝闵席季麻强贾路娄危江童颜郭梅盛林刁钟徐邱骆高夏蔡田樊胡凌霍'
    '虞万支柯昝管卢莫经房裘缪干解应宗丁宣贲邓郁单杭洪包诸左石崔吉钮龚'
    '和嵇邢滑裴陆荣翁荀羊於惠甄麴家封芮羿储靳汲邴糜松井段富巫乌焦巴弓'
    '牧隗山谷车侯宓蓬全郗班仰秋仲伊宫宁仇栾暴甘钭厉戎祖武符刘景詹束龙'
    '叶幸司韶郜黎蓟薄印宿白怀蒲邰从鄂索咸籍赖卓蔺屠蒙池乔阴郁胥能苍双'
    '闻莘党翟谭贡劳逄姬申扶堵冉宰郦雍舄璩桑桂濮牛寿通边扈燕冀郏浦尚农'
    '温别庄晏柴瞿阎充慕连茹习宦艾鱼容向古易慎戈廖庾终暨居衡步都耿满弘'
    '匡国文寇广禄阙东殴殳沃利蔚越夔隆师巩厍聂晁勾敖融冷訾辛阚那简饶空'


)


first_names = {
    'male':[
        '晓睿','宇晗','飞玉','安乐','飞铭','方沛','清舜','依儒','秀峰','铭瑞',
        '玄礼','政宸','秉成','建锋','抒志','志君','玄志','熹宜','锦平','济森',
        '鸿楷','柏行','吉聪','宇涵','缙博','奇坤','南邦','昌才','建通','方睿',
        '圣哲','樟锴','传亮','立圣','钟霖','林智','宇函','明聪','承淇','其道',
        '抒恺','筱暄','佳腾','圣佑','锋民','守钊','亦远','华淇','方泰','建达',
        '浩敬','章裕','文进','熹德','梓茂','熹卓','奇翰','咏铭','振冬','思杰',
        '抒杰','惠洛','承刚','天誉','彦华','蒽博','哲鑫','炜亮','旭惠','君浩',
        '明杭','进圣','瀚逸','佳善','秉韬','锐可','金金','昌晟','遵亭','政远',

    ],
    'female':[
        '梦洁','可琳','慧然','星妍','芸熙','天瑜','婧琪','冰露','尔珍','谷雪','乐萱','涵菡','海莲',
        '易梦','惜雪','宛海','之柔','亦瑶','妙菡','紫蓝','幻柏','元风','冰枫','芷蕊','凡蕾','凡柔',
        '安蕾','天荷','含玉','书兰','雅琴','书瑶','念芹','幻珊','谷丝','白晴','海露','书蕾','灵雁',
        '雪青','乐瑶','涵双','雅蕊','灵薇','含蕾','从梦','从蓉','语芙','夏彤','凌瑶','忆翠','幻灵',
        '怜菡','紫南','依珊','妙竹','怜蕾','映寒','惜霜','凌香','芷蕾','雁卉','迎梦','紫真','千青',
        '凌寒','紫安','寒安','怀蕊','秋荷','涵雁','语蝶','依波','晓旋','念之','盼芙','曼安','采珊',
        '初柳','迎天','曼安','南珍','妙芙','语柳','含莲','晓筠','夏山','尔容','念梦','傲南','问薇',
        '雨灵','凝安','羽馨','婕珍','佳琦','韵寒','博嘉','诗珊','雅霜',]
}

def gen_rand_name():
        last_name = random.choice(last_names)

        sex = random.choice(list(first_names.keys()))


        first_name = random.choice(first_names.get(sex))

        name = ''.join([last_name,first_name])

        print(name,sex)
        return name,sex

def create_robot(n):
    for i in range(n):
        name,sex = gen_rand_name()
        try:
            User.objects.create(phonenum=random.randint(21000000000,21900000000),
                                nickname=name,
                                sex=sex,
                                birth_year=random.randint(1970,2018),
                                birth_month=random.randint(1,12),
                                birth_day=random.randint(1,28),
                                location=random.choice(['bj','sh','gz','sz','cd','xa','wh','zz','nj','xm','hz','sy'])
                                )
            print('created:%s %s'%(name,sex))
        except django.db.utils.IntegrityError:
            pass


if __name__ == '__main__':
    create_robot(5000)
