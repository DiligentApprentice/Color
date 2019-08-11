from test_plus.test import TestCase

from color.articles.models import Articles

class TestArticles(TestCase):
    '''文章model测试'''

    def setUp(self):
        self.user = self.make_user()
        self.articles1 = Articles.objects.create(user=self.user,
                                                 title='文章一',
                                                 content='文章内容',
                                                 article_type=2,
                                                 tags='color')
        self.drafts = Articles.objects.create(user=self.user,
                                                 title='草稿',
                                                 content='草稿内容',
                                                 article_type=1,
                                                 tags='color')

    def test_instance(self):
        assert self.articles1 in Articles.objects.get_all_published_articles()
        assert self.drafts in Articles.objects.get_all_draft_articles()

    def test___str__(self):
        assert self.articles1.__str__() == '文章一'

