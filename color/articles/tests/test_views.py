import tempfile
from test_plus.test import TestCase
from PIL import Image

from django.test.client import Client
from django.urls import reverse

from color.articles.models import Articles

class TestArticleView(TestCase):
    '''文章view测试用例'''
    @staticmethod
    def create_tep_image():
        '''创建并读取一个临时图片'''
        size = (200, 200)
        color = (255,0,0,0)
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            image = Image.new('RGB', size, color)
            image.save(f, "PNG")
        return open(f.name ,'rb')

    def setUp(self):
        self.user = self.make_user()
        self.client = Client()
        self.client.login(username = self.user.username, password="password")
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
        self.test_image = self.create_tep_image()

    def test_article_list_view(self):
        response = self.client.get(reverse('articles:list'))
        assert response.status_code == 200
        assert Articles.objects.all().count() == 2
        assert self.articles1 in response.context["articles"]

    def test_create_article_view(self):
        response = self.client.post(reverse('articles:write_draft'),{"title":'文章二',
                                                                     "content":'文章内容二',
                                                                     "image":self.test_image,
                                                                     "tags":'标签'} )
        assert response.status_code == 302
        assert Articles.objects.all().count() == 3

    def tearDown(self):
        """测试结束时关闭临时文件"""
        self.test_image.close()










