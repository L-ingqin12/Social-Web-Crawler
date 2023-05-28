class WeiboUser:
    def __init__(self, id, nickname=None, gender=None, description=None, verified_reason=None, weibo_num=0, following=0,
                 followers=0):
        self.id = id
        self.nickname = nickname  # screen_name
        self.gender = "female" if gender == 'f' else "male"  # gender
        self.description = description  # description
        self.verified_reason = verified_reason

        self.weibo_num = weibo_num  # statuses count
        self.following = following  # follow count
        self.followers = self.string_to_int(followers) if str(type(followers)) == "<class 'str'>" else int(
            followers)  # followers count  float(followers[:-1])*10000 万

    def list_all_members(self):
        result = ''
        for key, value in self.__dict__.items():
            # print("{}:{}".format(key, value))
            if value != None:
                result += "{}:{}\n".format(key, value)

        return result

    def __str__(self):
        """打印微博用户信息"""
        result = ''
        result += u'用户昵称: %s\n' % self.nickname
        result += u'用户id: %s\n' % self.id
        result += u'微博数: %d\n' % self.weibo_num
        result += u'关注数: %d\n' % self.following
        result += u'粉丝数: %d\n' % self.followers
        return result

    def string_to_int(self, string):
        """字符串转换为整数"""
        if isinstance(string, int):
            return string
        elif string.endswith(u'万+'):
            string = int(float(string[:-2]) * 10000)
        elif string.endswith(u'万'):
            string = int(float(string[:-1]) * 10000)
        return int(string)


class WeiboInfo:
    def __init__(self):
        self.id = ''
        self.user_id = ''

        self.content = ''

        self.retweet_pictures = None
        self.original = None

        self.publish_place = ''
        self.publish_time = ''
        self.publish_tool = ''

        self.up_num = 0
        self.retweet_num = 0
        self.comment_num = 0

    def list_all_members(self):
        result = ''
        for key, value in self.__dict__.items():
            # print("{}:{}".format(key, value))
            if value != None:
                result += "{}:{}\n".format(key, value)
        return result
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
