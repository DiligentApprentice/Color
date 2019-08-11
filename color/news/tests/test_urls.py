from test_plus.test import TestCase
from django.urls import resolve, reverse

from color.news.models import News

class TestUrls(TestCase):

    def setUp(self):
        self.user = self.make_user()
        self.news = News.objects.create(user=self.user, content='1111')

    def test_list_resolve(self):
        self.assertEqual(resolve('/news/newslist/').view_name, 'news:list')

    def test_list_reverse(self):
        self.assertEqual(reverse('news:list'), '/news/newslist/')

    def  test_post_news_resolve(self):
        self.assertEqual(resolve('/news/post-news/').view_name , 'news:post_news')

    def test_post_news_reverse(self):
        self.assertEqual(reverse('news:post_news'),'/news/post-news/')

    def test_like_resolve(self):
        self.assertEqual(resolve('/news/like/').view_name, 'news:like')

    def test_like_reverse(self):
        self.assertEqual(reverse('news:like'), '/news/like/')

    def test_comments_resolve(self):
        self.assertEqual(resolve('/news/get-thread/').view_name, 'news:comments')

    def test_comments_reverse(self):
        self.assertEqual(reverse('news:comments'), '/news/get-thread/')

    def test_post_comment_resolve(self):
        self.assertEqual(resolve('/news/post-comment/').view_name, 'news:post_comment')

    def test_post_comment_reverse(self):
        self.assertEqual(reverse('news:post_comment'), '/news/post-comment/')

    def test_delete_news_resolve(self):
        self.assertEqual(resolve('/news/delete/%s/'%(self.news.id)).view_name, 'news:delete_news')

    def test_delete_news_reverse(self):
        self.assertEqual(reverse('news:delete_news',kwargs={"pk":self.news.id}), '/news/delete/%s/'%(self.news.id))

