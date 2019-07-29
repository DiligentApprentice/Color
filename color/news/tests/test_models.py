from test_plus.test import TestCase

from news.models import News

class TestUser(TestCase):
    '''首页动态测试'''

    def setUp(self):
        self.user = self.make_user('user1')
        self.user2 = self.make_user('user2')
        self.news = News.objects.create(user=self.user,content='第一条动态')
        self.news2 = News.objects.create(user=self.user2, content='第二个调动态')
        self.reply = News.objects.create(user=self.user2,
                                         content='第二个用户给给第一条动态的评论',
                                         parent=self.news,
                                         reply=True )

    def test___str__(self):
        assert self.news.__str__() == '第一条动态'

    def test_like_or_cancle(self):
        self.news.like_or_cancle(self.user2)
        assert self.user2 in  self.news.get_likers()
        assert self.news.total_like_num() == 1

    def test_total_comment_num(self):
        assert self.news.total_comment_num()==1
        assert self.reply in self.news.get_all_relation_comments()




