from test_plus.test import TestCase, RequestFactory
from django.test import Client
from django.urls import reverse

from news.views import NewsListView, NewsDeleteVieww
from news.models import News


#重写学模拟浏览器发请求，验证验证视图类或者视图函数的返回结果


class TestNewsView(TestCase):

    def setUp(self):
        self.user = self.make_user('user1')
        self.user2 = self.make_user('user2')
        self.client = Client()
        self.client2 = Client()
        self.news = News.objects.create(user=self.user, content='第一条动态')
        self.news2 = News.objects.create(user=self.user2, content='第二条动态')
        self.reply = News.objects.create(user=self.user2, content='第一条动态的评论', reply=True, parent=self.news)
        self.client.login(username="user1", password="password")

    def test_list(self):
        response = self.client.get(reverse('news:list'))
        assert response.status_code == 200
        assert self.news in response.context["news_list"]
        assert  self.news2 in response.context["news_list"]
        assert self.reply not in response.context["news_list"]

    def test_post_news(self):
        response = self.client.post(reverse("news:post_news"),{"post":'新增加一条动态'}, HTTP_X_REQUESTED_WITH="XMLHttpRequest" )
        assert response.status_code == 200
        assert News.objects.filter(reply=False).count() == 3

    def test_post_like_or_cancle(self):
        response = self.client.post(reverse('news:like'), {"news": self.news2.id},HTTP_X_REQUESTED_WITH="XMLHttpRequest" )
        assert response.status_code == 200
        assert self.news2.total_like_num() ==1
        assert response.json()['likes'] == 1

    def test_post_comment(self):
        response = self.client.post(reverse('news:post_comment'),
                                    {"reply":'ok,fine',"parent":self.news2.id},
                                    HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response.status_code == 200
        assert self.news2.total_comment_num()==1
        assert response.json()['comments'] == 1


    def test_get_relation_comments(self):
        response = self.client.get(reverse('news:comments'),{"news":self.news.id},HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        assert response.status_code == 200
        assert self.news.total_comment_num() ==1

    def test_delete_news(self):
        response = self.client.post(reverse('news:delete_news',kwargs={"pk":self.news.id}))
        assert response.status_code == 302
        assert News.objects.filter(reply=False).count() == 1
















