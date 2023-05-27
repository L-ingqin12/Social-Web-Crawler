import time
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
import hashlib

import json
from tqdm import tqdm
from lib.encrypt import encrypt
from .data_analysis import remove_tags_emojis
from .lib.zhihu_data import ZhihuUser


class ZhihuApi(object):

    def __init__(self):
        '''
        # 使用nodejs加载加密生成
        self.node = execjs.get()

        with open(r'lib\zhihu_encrypt.js', encoding='utf-8') as f:
            js_code = f.read()
        self.ctx = self.node.compile(js_code,
                                     cwd=r'..\node_modules')
        '''

        self.session = requests.session()
        headers = {
            "Host": "www.zhihu.com",
            'x-api-version': '3.0.91',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/84.0.4147.135 Safari/537.36',
            # "Authorization": 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'x-app-za': 'OS=Web'
        }
        self.session.headers = headers

    # 获取话题讨论信息
    def topic_get(self, topic_id, type="timeline_activity", limit=20, offset=0):  # type="essence"
        """
        获取话题的讨论信息
        :param topic_id: 话题的详情
        :param type: 获取的话题信息排序方式 timeline_activity顺时间线 essence按照讨论热度
        :param limit:
        :param offset:
        :return:
        """
        session = self.session
        base_url = f'https://www.zhihu.com/api/v4/topics/{topic_id}/feeds/{type}?include=data%5B%3F%28target.type' \
                   f'%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target.content' \
                   f'%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%3F' \
                   f'%28target.type%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Danswer%29%5D.target' \
                   f'.is_normal%2Ccomment_count%2Cvoteup_count%2Ccontent%2Crelevant_info%2Cexcerpt.author.badge%5B%3F' \
                   f'%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dtopic_sticky_module%29%5D' \
                   f'.target.data%5B%3F%28target.type%3Darticle%29%5D.target.content%2Cvoteup_count%2Ccomment_count' \
                   f'%2Cvoting%2Cauthor.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type' \
                   f'%3Dtopic_sticky_module%29%5D.target.data%5B%3F%28target.type%3Dpeople%29%5D.target.answer_count' \
                   f'%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type' \
                   f'%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Danswer%29%5D.target.annotation_detail' \
                   f'%2Ccontent%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B' \
                   f'%3F%28target.type%3Danswer%29%5D.target.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics' \
                   f'%3Bdata%5B%3F%28target.type%3Darticle%29%5D.target.annotation_detail%2Ccontent%2Cauthor.badge%5B' \
                   f'%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B%3F%28target.type%3Dquestion%29%5D.target' \
                   f'.annotation_detail%2Ccomment_count&limit={limit}&offset={offset}'

        response = session.get(base_url)
        return response.json()

    def get_user_profile(self, user_id):
        """
        获取用户信息
        :param user_id:
        :return:
        """
        session = self.session
        base_url = f"https://www.zhihu.com/api/v4/members/{user_id}?include=locations,employments,gender,educations," \
                   f"business,voteup_count,thanked_Count,follower_count,following_count,cover_url," \
                   f"following_topic_count,following_question_count,following_favlists_count,following_columns_count," \
                   f"avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count," \
                   f"commercial_question_count,favorite_count,favorited_count,logs_count,included_answers_count," \
                   f"included_articles_count,included_text,message_thread_token,account_status,is_active," \
                   f"is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name," \
                   f"show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,is_org_createpin_white_user," \
                   f"mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count," \
                   f"thanked_count,description,hosted_live_count,participated_live_count,allow_message," \
                   f"industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics"
        response = session.get(base_url)
        return response.json()

    def following_info(self, user_id, offset=0, limit=20):
        """
        获取关注者情况
        :param user_id:
        :param offset:
        :param limit:
        :return:
        """
        session = self.session
        base_url = f"https://www.zhihu.com/api/v4/members/{user_id}/followees?include=answer_count%2Carticles_count" \
                   f"%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type%3Dbest_answerer%29" \
                   f"%5D.topics&limit={limit}&offset={offset}"
        session.get(f"https://www.zhihu.com/people/{user_id}/followers")
        session.headers.update({"Referer": f"https://www.zhihu.com/people/{user_id}/followers"})
        self.get_x_zse_96(session=session, url=base_url)
        response = session.get(base_url)
        return response.json()

    def get_x_zse_96(self, session, url):
        """
        生成知乎的x-zse-96参数
        :param session: 主要是用来获取session中cookie的dc_0参数和对于session的header参数进行修改
        :param url: 生成参数时用到了请求的参数路径
        :return:
        """
        d_c0 = session.cookies.get("d_c0")
        x_zse_93 = '101_3_3.0'
        session.headers.update({"x-zse-93": x_zse_93})
        code = url.replace("https://www.zhihu.com", "")
        s = '+'.join([x_zse_93, code, d_c0])
        md5_s = hashlib.md5(s.encode()).hexdigest()
        # b_s = self.ctx.call("D", md5_s)
        b_s = encrypt(md5_s)
        x_zse_96 = '2.0_' + b_s
        session.headers.update({"x-zse-96": x_zse_96})
        return x_zse_96

    def follower_info(self, user_id, offset=0, limit=20):
        """
        获取知乎粉丝列表
        :param user_id: 用户id
        :param offset:
        :param limit:
        :return:
        """
        session = self.session
        base_url = f"https://www.zhihu.com/api/v4/members/{user_id}/followers?include=data%5B*%5D.answer_count" \
                   f"%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F%28type" \
                   f"%3Dbest_answerer%29%5D.topics&offset={offset}&limit={limit}"
        session.get(f"https://www.zhihu.com/people/{user_id}/followers")
        session.headers.update({"Referer": f"https://www.zhihu.com/people/{user_id}/followers"})
        self.get_x_zse_96(session=session, url=base_url)
        response = session.get(base_url)
        return response.json()

    def get_hotlist(self):
        """
        获取知乎热榜
        :return:
        """
        base_url = "https://www.zhihu.com/api/v3/explore/guest/feeds?limit=50"
        response = requests.get(base_url)
        return response.json()

    # 获取问题讨论详情
    def get_question_answer(self, question_id, offset=0, limit=20, sort_by="default"):
        """
        获取问题讨论详情
        :param question_id: 问题的id
        :param offset:
        :param limit:
        :param sort_by: 获取信息的排序方式 updated 按时间排序 默认排序方式
        :return:
        """
        session = self.session
        include = "data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action" \
                  "%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count" \
                  "%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings" \
                  "%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion" \
                  "%2Cexcerpt%2Cis_labeled%2Cpaid_info%2Cpaid_info_content%2Crelationship.is_authorized%2Cis_author" \
                  "%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B" \
                  "*%5D.author.follower_count%2Cbadge%5B*%5D.topics%3Bdata%5B*%5D.settings.table_of_content.enabled"
        base_url = f"https://www.zhihu.com/api/v4/questions/{question_id}/answers?include={include}&limit={limit}&offset={offset}&platform=desktop&sort_by={sort_by}"

        session.get(f"https://www.zhihu.com/question/{question_id}")
        session.headers.update({"Referer": f"https://www.zhihu.com/question/{question_id}"})
        self.get_x_zse_96(session=session, url=base_url)
        response = session.get(base_url)
        return response.json()

    # 获取问答的评论信息 get_answer_reviews 、 get_root_comments 、 get_child_reviews
    def get_child_comments(self, session, comment_id, limit=20, offset=""):
        """
        获取子评论的详情
        :param session:
        :param comment_id: 父级评论信息的id
        :param limit:
        :param offset:
        :return:
        """
        base_url = f"https://www.zhihu.com/api/v4/comment_v5/comment/{comment_id}/child_comment?order_by=ts&limit=2{limit}&offset={offset}"
        self.get_x_zse_96(session=session, url=base_url)
        response = session.get(base_url)
        return response.json()

    def get_root_comments(self, session, answer_id, limit=20, offset=""):
        """
        获取父级评论信息详情
        :param session:
        :param answer_id: 评论信息所属的回答
        :param limit:
        :param offset:
        :return:
        """
        base_url = f"https://www.zhihu.com/api/v4/comment_v5/answers/{answer_id}/root_comment?order_by=score&limit={limit}&offset={offset}"
        self.get_x_zse_96(session=session, url=base_url)
        response = session.get(base_url)

        return response.json()

    def get_answer_reviews(self, question_id, answer_id):
        """
        获取评论信息来自的回答
        :param question_id: 问题的id信息 结合知乎热榜可以获得
        :param answer_id: 回答的id信息 结合知乎回答详情可以获得
        :return:
        """
        session = self.session
        session.get(f"https://www.zhihu.com/question/{question_id}")
        session.headers.update({"Referer": f"https://www.zhihu.com/question/{question_id}"})
        data = self.get_root_comments(session, answer_id)
        is_end = False
        root_comments = data['data']
        page = data['paging']
        total = page['totals']
        # print(total)
        # tqdm 进度条
        with tqdm(total=100, desc='comment_get', leave=True, ncols=100, unit='B', unit_scale=True) as pbar:
            review = []
            while not is_end:
                # print("主",root_comments)
                for root_comment in root_comments:
                    pbar.update(1 / total * 100 if total != 0 else total)
                    # print(root_comment)
                    comment_id = root_comment['id']
                    if "child_comments" in root_comment:
                        root_comment.pop("child_comments")
                    # else:
                    review.append(root_comment)
                    child_comment_is_end = False
                    child_data = self.get_child_comments(session, comment_id)
                    child_page = child_data['paging']
                    # child_total = child_page['totals']
                    child_comments = child_data['data']
                    # print(child_total)
                    # with tqdm(total=child_total, desc='child_comment_get', leave=True, ncols=100, unit='B',
                    #           unit_scale=True) as pbar2:

                    while not child_comment_is_end:
                        # print("子",child_comments)
                        # pbar.update(20 / child_total * 100 if child_total !=0 else child_total)
                        for child_comment in child_comments:
                            # print(child_comment)
                            pbar.update(1 / total * 100 if total != 0 else total)
                            if "child_comments" in child_comment:
                                child_comment.pop("child_comments")
                            # else:
                            review.append(child_comment)
                        next_child_url = child_page['next']
                        next_child_offset = next_child_url.split("=")[2].split("&")[0]
                        next_child_limit = next_child_url.split("=")[1].split("&")[0]
                        child_comment_is_end = child_page['is_end']
                        if not child_comment_is_end:
                            child_data = self.get_child_comments(session, comment_id, offset=next_child_offset,
                                                                 limit=next_child_limit)
                            # pbar2.update(int(next_child_limit)/child_total)
                            child_page = child_data['paging']
                            child_comments = child_data['data']
                        time.sleep(0.5)
                next_url = page['next']
                next_offset = next_url.split("=")[2].split("&")[0]
                next_limit = next_url.split("=")[1].split("&")[0]
                is_end = page['is_end']
                if not is_end:
                    data = self.get_root_comments(session, answer_id, offset=next_offset, limit=next_limit)
                    # pbar.update(int(next_limit) / total * 100)
                    page = data['paging']
                    root_comments = data['data']

        return review

    def get_activities(self, user_id, offset=0, page=None):
        """
        获取用户动态
        :param user_id: 用户id
        :param offset: 动态获取的偏移量
        :param page: 动态的页数
        :return:
        """
        session = self.session
        base_url = f"https://www.zhihu.com/api/v3/moments/{user_id}/activities?offset={offset}&limit=8&desktop=true" if page != None else f"https://www.zhihu.com/api/v3/moments/{user_id}/activities?offset={offset}&page_num=1"
        session.get(f"https://www.zhihu.com/people/{user_id}")
        session.headers.update({"Referer": f"https://www.zhihu.com/people/{user_id}"})
        self.get_x_zse_96(session, base_url)
        response = session.get(base_url)
        return response.json()

    def get_user_answer(self, user_id, offset=0, limit=20, sort_by="created"):
        """
        获取用户的所有回答
        :param user_id: 用户id
        :param offset: 评论获取偏移量
        :param limit: 获取评论条数限制
        :param sort_by: created 回答时间 voteups 点赞量
        :return:
        """
        session = self.session
        include = "data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cattachment%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Creview_info%2Cexcerpt%2Cpaid_info%2Creaction_instruction%2Cis_labeled%2Clabel_info%2Crelationship.is_authorized%2Cvoting%2Cis_author%2Cis_thanked%2Cis_nothelp%2Cis_recognized%3Bdata%5B*%5D.vessay_info%3Bdata%5B*%5D.author.badge%5B%3F%28type%3Dbest_answerer%29%5D.topics%3Bdata%5B*%5D.author.vip_info%3Bdata%5B*%5D.question.has_publishing_draft%2Crelationship"
        base_url = f"https://www.zhihu.com/api/v4/members/{user_id}/answers?include={include}&offset={offset}&limit={limit}&sort_by={sort_by}"
        session.get(f"https://www.zhihu.com/people/{user_id}/answers")
        session.headers.update({"Referer": "https://www.zhihu.com/people/{user_id}/answers"})
        self.get_x_zse_96(session, base_url)
        response = session.get(base_url)
        return response.json()


api = ZhihuApi()


def format_time(datestr):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(datestr))


def comment_simple_analysis(answer_id="3021348829", question_id="599787027"):
    # 评论数据分析
    ip_from = defaultdict(int)
    gender_info = defaultdict(int)
    contents = ''
    user_type_count = defaultdict(int)
    time_list = []
    review_answers = api.get_answer_reviews(answer_id=answer_id, question_id=question_id)
    for review_answer in review_answers:
        # print(json.dumps(review_answer, sort_keys=True, indent=4,separators=(',', ':'), ensure_ascii=False))
        created_time = format_time(review_answer['created_time'])
        time_list.append(created_time)
        content = review_answer['content']
        contents += content
        comment_tag = review_answer['comment_tag']
        ip = comment_tag[0]['text'].replace('IP 属地', '') if comment_tag[0]['type'] == 'ip_info' else "未识别"
        ip_from[ip] += 1
        author = review_answer['author']
        gender = author['gender']
        if gender == 0:
            gender = 'undefined'
        elif gender == 1:
            gender = 'male'
        elif gender == 2:
            gender = 'female'
        else:
            gender = "unknown"
        gender_info[gender] += 1
        user_id = author['url_token']
        user_name = author['name']
        user_info = author['headline']  # 个人简介
        user_type = author['type']
        user_type_count[user_type] += 1
        print(created_time, content, ip, gender, user_name, user_id, user_type, user_info)

    return {"time_list": list(time_list),
            "ip_from": dict(ip_from),
            "gender_count": dict(gender_info),
            "user_type_count": dict(user_type_count),
            "contents:": contents}


def user_activities(user_id="lu-xin-qiong"):
    # 解析用户动态
    data = api.get_activities(user_id=user_id, offset=8)
    activities = data['data']
    page = data['paging']
    is_end = False
    all_activities = []
    all_activities.extend(activities)
    while not is_end:
        for activity in activities:
            created_time = activity['created_time']
            print(format_time(created_time))
            if activity['action_text'] == "回答了问题" or activity['action_text'] == "赞同了回答":
                print(activity['action_text'], activity['target']['question']['title'])
            elif activity['action_text'] == "赞同了文章" or activity['action_text'] == "关注了问题":
                print(activity['action_text'], activity['target']['title'])
            # elif activity['action_text']=="赞同了回答":
            elif "关注了" in activity['action_text']:
                if "话题" not in activity['action_text'] and "问题" not in activity['action_text']:
                    print(activity['action_text'], activity['target']['name'])
            elif "发布了想法" == activity['action_text']:
                print(activity['action_text'], activity['target']['content'][0]['content'])
            else:
                print(activity['action_text'], activity['target'])
        next_url = page['next']
        # print(next_url)
        next_offset = next_url.split('=')[1].split('&')[0]
        # (?<=offset=)\d+_\d+_\d+(?=&)
        next_page = next_url.split('=')[2]
        # (?<=limit=)\d+(?=&)
        # print(next_page)
        is_end = page['is_end']
        data = api.get_activities(user_id=user_id, offset=next_offset, page=next_page)
        activities = data['data']
        all_activities.extend(activities)
        activities.pop(0)
        page = data['paging']

    return all_activities

def print_user(user_id = "zhiyiYo"):
    info = api.get_user_profile(user_id=user_id)
    user = ZhihuUser(user_id=user_id, name=info["name"], gender=info["gender"], following=info["following_count"],
                     follower=info["follower_count"], description=info["description"],
                     answer_count=info["answer_count"],
                     articles_count=info["articles_count"], ip_info=info["ip_info"], thank_count=info["thanked_count"],
                     type=info["type"], voteup_count=info["voteup_count"], headline=info["headline"],
                     following_favlists_count=info["following_favlists_count"],
                     following_question_count=info["following_question_count"],
                     following_topic_count=info["following_topic_count"],
                     following_columns_count=info["following_columns_count"], question_count=info["question_count"],
                     pins_count=info["pins_count"], favorite_count=info["favorite_count"],
                     favorited_count=info["favorited_count"])
    print(user)
    return info

def hot_list_format():
    hot_list= api.get_hotlist()['data']
    for hot in hot_list:
        actor= hot['actors'][0]
        print(actor['id'],actor['name'],actor['introduction'])
        info = hot['target']
        create_time = format_time(hot['created_time'])
        print(create_time)
        print(remove_tags_emojis(info['content']))
        print(info['id'],info["question"]['answer_count'],info['author']['name'],info['author']['url_token'] if info['author']['name']!='匿名用户' else '')

if __name__ == "__main__":
    # print(json.dumps(api.get_question_answer(question_id="599787027", offset=150), sort_keys=True, indent=4,
    #                  separators=(',', ':'), ensure_ascii=False))

    # print(json.dumps(api.get_user_answer(user_id="zhiyiYo"), sort_keys=True, indent=4,
    #                  separators=(',', ':'), ensure_ascii=False))
    # print(json.dumps(api.get_user_answer(user_id="zhiyiYo"), sort_keys=True, indent=4,
    #                  separators=(',', ':'), ensure_ascii=False))
    # print(json.dumps(api.get_hotlist(), sort_keys=True, indent=4,
    #                  separators=(',', ':'), ensure_ascii=False))
    #
    hot_list_format()
    # 获取用户信息
    # print_user(user_id="zhiyi")

    """
    # init文档读取
    import inspect
    init_docstring = inspect.getdoc(user.__init__)
    for param in init_docstring.split('\n'):
        print(param.split())
    print(init_docstring)
    """
    """

    """

    """

    """
