# app_key="93966320"
# app_secret="88f8a613538ad114cc948225aa347c2a"
import urllib.parse
from collections import defaultdict
import time
import random

import requests
import json


class WeiboApi(object):

    def __init__(self):
        self.session = requests.session()

        cookie = '_T_WM=20139464994; MLOGIN=1; __bid_n=18856521382ad479214207; ' \
                 'FPTOKEN=BEuUuLntHRLBfjN+wnBDXZwwqnnT+uwvuol3l/8yU5yV0iw95fcU7NOivb8Wx3Zc9urkJIxx9U5' \
                 '+kiqKffHwq0rHkgsrB6sjrK/+XoDYdWBTaejfSyFNQbXS8uzzk1GZtqGs9g0C+OCHMUaPIssBb7b/EnszlBhXn8' \
                 '/UFTpi4lMnGRa3V+leQClhRLXpYwpMrJxxvM9P1QCg2t26tGvgEC5uhX+i6SNBsAnXFkoftLGTcQdsQxnkwa' \
                 '/ie1Rj3h3jhvZqV1ODY5qsXj+hTO6A+XDlkfrSq+vzTU56KCSW4GalP' \
                 '/dVOs6pnw9vOK4Lr6QzMVMzFH1B8cxr0k3AK5eqF5IGQ3B6ZHfk00A3Div5r05N' \
                 '/xtvHZd6eeIKZ629FdYHhn3hL68boLR2jUkk7NrhaQ==|9yyXZWWFa3n41QtJvuwmCjzswMRuN+O9+4xG2w3KfcY=|10' \
                 '|156a19941c490e4dfd3879acfb6c63af; ' \
                 'SUB=_2A25JdBztDeRhGeFM7FIS9yjPzTqIHXVqlqSlrDV6PUJbktAGLRKtkW1NQKiTiZ3vkoL9ul1-Sv9DqR19LroTtHpy; ' \
                 'SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFvoFEjE2Wq52MNGxobw62m5NHD95QNeoM7e0Mce0qcWs4DqcjDi--ci-20i' \
                 '-20i--ci-20i-27i--Xi-z4iKyFi--RiKyWi-zpeo5pS05t; SSOLoginState=1685089469'

        headers = {
            "Host": "m.weibo.cn",
            'MWeibo-Pwa': '1',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1',
            'Cookie': cookie,
        }
        self.session.headers = headers

    def get_json(self, params):
        """获取网页中json数据"""
        if type(params)=="<class 'dict'>":
            url = 'https://m.weibo.cn/api/container/getIndex?'
            r = requests.get(url, params=params)
        else:
            url = f'https://m.weibo.cn/api/container/getIndex?{params}'
            r=requests.get(url)
        return r.json()

    def get_weibo_json(self, container_id, page):
        """获取网页中微博json数据"""
        # params = {'containerid': '107603' + str(self.user_id), 'page': page}
        params = {'containerid': container_id, 'page': page}
        js = self.get_json(params)
        return js

    def string_to_int(self, string):
        """字符串转换为整数"""
        if isinstance(string, int):
            return string
        elif string.endswith(u'万+'):
            string = int(string[:-2] + '0000')
        elif string.endswith(u'万'):
            string = int(string[:-1] + '0000')
        return int(string)

    def get_hot(self):
        """
        微博热点,每分钟更新一次
        :return:
        """
        session = self.session
        params = "containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE" \
                 "%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0" \
                 "%26c_type%3D30%26display_time%3D1540538388&luicode=10000011&lfid=231583"
        base_url = f"https://m.weibo.cn/api/container/getIndex?{params}"
        session.headers.update({'Referer': 'https://s.weibo.com/top/summary?cate=realtimehot'})
        response = session.get(base_url)
        return response.json()

    # def get_search(self,params):
    #

    def get_user(self, uid):
        session = self.session
        base_url = f"https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}"
        session.headers.update({'Referer': f'https://m.weibo.cn/u/{uid}'})
        response = session.get(base_url)
        return response.json()

    def get_weibo_info(self, weibo_id):
        session = self.session
        response = session.get(f'https://m.weibo.cn/detail/{weibo_id}')  # 4806418774099867
        # print(response.text)
        # selector = etree.HTML(response.text)
        html = response.text
        # print(html)
        html = html[html.find('"status":'):]
        html = html[:html.rfind('"call"')]
        html = html[:html.rfind(',')]
        html = '{' + html + '}'
        # print (html)
        json_data = json.loads(html, strict=False)
        return json_data

    def get_weibo_comments(self, weibo_id, page=1, max_id=1):

        url = f'https://m.weibo.cn/comments/hotflow?id={weibo_id}&mid={weibo_id}&max_id_type=0{"&max_id={}".format(max_id) if page != 1 else ""}'
        session = self.session
        session.get(f'https://m.weibo.cn/detail/{weibo_id}')
        session.headers.update({'Referer': f'https://m.weibo.cn/detail/{weibo_id}'})

        response = session.get(url)
        return response.json()

    """
    #  需要token
    def get_user_timeline(self, uid):
        session = self.session
        url = f'https://m.weibo.cn/api/container/getIndex?type=uid&value={uid}'
        session.headers.update({'Referer':'https://m.weibo.cn/'})
        response = session.get(url)
        return response.json()
    """


weibo = WeiboApi()


def date_format(time_str):
    import datetime
    # 将时间字符串转换为 datetime 对象
    time_obj = datetime.datetime.strptime(time_str, '%a %b %d %H:%M:%S %z %Y')

    # 将 datetime 对象转换为指定格式的时间字符串
    formatted_time_str = time_obj.strftime('%Y-%m-%d %H:%M:%S')

    return formatted_time_str


def get_all_comment_weibo(weibo_id='4806418774099867'):
    comments = []
    first = weibo.get_weibo_comments(weibo_id=weibo_id, page=1)
    if first['ok'] == 1:
        comments.extend(first['data']['data'])
        # print(first)
        while first['data']['max_id'] != 0:
            print(first)
            max_id = first['data']['max_id']
            first = weibo.get_weibo_comments(weibo_id=weibo_id, page=2, max_id=max_id)
            time.sleep(random.randint(2, 7))
            if first['ok'] == 1:
                # print(first)
                comments.extend(first['data']['data'])
            else:
                try:
                    # i = 3
                    # while first['ok'] != 1:
                    time.sleep(random.randint(2, 7))
                    first = weibo.get_weibo_comments(weibo_id=weibo_id, page=2, max_id=max_id)
                    if first['ok'] == 1:
                        # print(first)
                        comments.extend(first['data']['data'])
                        # break
                    # if i == 0:
                    else:
                        raise Exception("something error happened, data is not all of this theme")
                        # i -= 1

                except Exception as e:
                    print('traceback:', e.args[0])
                    return comments

    else:
        print("something error happened")
    return comments


def weibo_comments_simple_analysis(weibo_id="4806418774099867"):
    gender_count = defaultdict(int)
    provinces_count = defaultdict(int)
    time_list = []
    contexts = ''
    comments = get_all_comment_weibo(weibo_id)
    for comment in comments:
        # print(comment)
        id = comment['id']
        create_time = date_format(comment['created_at'])
        time_list.append(create_time)
        context = comment['text']
        province = comment['source'].replace('来自', '')
        provinces_count[province] += 1
        contexts += context
        user = comment['user']
        user_id = user['id']
        nickname = user['screen_name']
        description = user['description']
        gender = user['gender']
        gender_count[gender] += 1
        # verified_reason = user['verified_reason']
        print(id, create_time, province, context, user_id, nickname, description, gender)

    male = gender_count['m']
    female = gender_count['f']
    gender_count.pop('f')
    gender_count.pop('m')
    gender_count.update({'male': male, 'female': female})

    return {
        'time_list': time_list,
        'gender_count': dict(gender_count),
        'provinces_count': dict(provinces_count),
        'context': contexts
    }


def hotlist_info():
    hot_list = weibo.get_hot()['data']['cards'][0]['card_group']
    print(hot_list)
    for hot in hot_list:
        print(hot['desc'],end =' ')
        if 'desc_extr' in hot:
            print(hot['desc_extr'])
        print(hot['scheme'])
        scheme=hot['scheme'].split('?')[1]
        # params = urllib.parse.parse_qs(scheme)
        # data=weibo.get_json(scheme)

        # print(data)


if __name__ == '__main__':
    weibo = WeiboApi()

    # # weibo.session=wblogin()
    print(json.dumps(weibo.get_user(uid=1900698023),
                     sort_keys=True, indent=4,
                     separators=(',', ':'), ensure_ascii=False))
    #
    # # print(weibo_comments_simple_analysis(weibo_id='4905352364036293'))

    # hotlist_info()
    """
    # 热搜榜
    hot = weibo.get_hot()
    for data in hot['data']['cards'][0]['card_group']:

        print(data['desc'],data['scheme'])
        if 'desc_extr' in data:
            print(data['desc_extr'],

    """
