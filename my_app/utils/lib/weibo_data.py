class WeiboUser:
    def __init__(self):
        self.id = ''
        self.nickname = ''  # screen_name
        self.gender = ''  # gender
        # self.location = ''
        # self.birthday = ''
        self.description = ''  # description
        self.verified_reason = ''
        # self.talent = ''
        # self.education = ''
        # self.work = ''
        self.weibo_num = 0  # statuses count
        self.following = 0  # follow count
        self.followers = 0  # followers count  float(followers[:-1])*10000 万

    def __str__(self):
        """打印微博用户信息"""
        result = ''
        result += u'用户昵称: %s\n' % self.nickname
        result += u'用户id: %s\n' % self.id
        result += u'微博数: %d\n' % self.weibo_num
        result += u'关注数: %d\n' % self.following
        result += u'粉丝数: %d\n' % self.followers
        return result


class WeiboInfo:
    def __init__(self):
        self.id = ''
        self.user_id = ''

        self.content = ''
        self.article_url = ''

        self.original_pictures = []
        self.retweet_pictures = None
        self.original = None
        self.video_url = ''

        self.publish_place = ''
        self.publish_time = ''
        self.publish_tool = ''

        self.up_num = 0
        self.retweet_num = 0
        self.comment_num = 0

    def __str__(self):
        """打印一条微博"""
        result = self.content + '\n'
        result += u'微博发布位置：%s\n' % self.publish_place
        result += u'发布时间：%s\n' % self.publish_time
        result += u'发布工具：%s\n' % self.publish_tool
        result += u'点赞数：%d\n' % self.up_num
        result += u'转发数：%d\n' % self.retweet_num
        result += u'评论数：%d\n' % self.comment_num
        result += u'url：https://weibo.cn/comment/%s\n' % self.id
        return result
