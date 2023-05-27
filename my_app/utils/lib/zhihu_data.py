class ZhihuUser:
    def __init__(self, user_id='', name='', gender='', following=0, follower=0, description=None, answer_count=0,
                 articles_count=0,
                 ip_info=None, thank_count=None, type=None, voteup_count=None, headline=None,
                 following_favlists_count=0, following_question_count=0, following_topic_count=0,
                 following_columns_count=0, question_count=0, columns_count=0, pins_count=0, favorite_count=0,
                 favorited_count=0):
        """
        知乎用户信息列表
        :param user_id: 用户id
        :param name: 昵称
        :param gender: 性别
        :param following: 关注数量
        :param follower: 粉丝数量
        :param description: 个人描述
        :param answer_count: 回答统计
        :param articles_count: 文章数量统计
        :param ip_info: ip属地
        :param thank_count: 获得用户喜欢数量
        :param type: 用户类型
        :param voteup_count:获得赞同数量
        :param headline: 用户标题
        :param following_favlists_count: 关注收藏夹数量
        :param following_question_count: 关注问题数量
        :param following_topic_count: 关注话题数量
        :param following_columns_count: 关注专栏数量
        :param question_count: 提问数量
        :param columns_count: 专栏数量
        :param pins_count: 想法数量
        :param favorite_count: 收藏夹数量
        :param favorited_count: 被收藏数量
        """
        self.user_id = user_id
        self.name = name
        self.gender = gender
        self.following = following
        self.follower = follower
        self.description = description
        self.answer_count = answer_count
        self.articles_count = articles_count
        self.ip_info = ip_info
        self.thank_count = thank_count
        self.type = type
        self.voteup_count = voteup_count
        self.headline = headline
        self.following_favlists_count = following_favlists_count
        self.following_question_count = following_question_count
        self.following_topic_count = following_topic_count
        self.following_columns_count = following_columns_count
        self.question_count = question_count
        self.columns_count = columns_count
        self.pins_count = pins_count
        self.favorite_count = favorite_count
        self.favorited_count = favorited_count

    def list_all_members(self):

        for key, value in self.__dict__.items():
            print("{}:{}".format(key, value))

    def __str__(self):
        """打印知乎用户"""
        result = ''
        result += u'用户昵称: %s\n' % self.name
        result += u'用户id: %s\n' % self.user_id
        result += u'ip属地: %s\n' % self.ip_info
        result += u'关注数: %d\n' % self.following
        result += u'粉丝数: %d\n' % self.follower
        return result
