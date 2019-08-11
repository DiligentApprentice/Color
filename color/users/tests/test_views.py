from test_plus.test import TestCase, RequestFactory

from color.users.views import UserUpdateView

class TestBase(TestCase):
    '''测试基类'''

    def setUp(self):
        self.user = self.make_user()
        self.factory = RequestFactory()


class TestUserUpdateView(TestBase):
    '''用户修改视图测试'''

    def setUp(self):
        super(TestUserUpdateView,self).setUp()
        request = self.factory.get('/index')
        self.view = UserUpdateView()
        request.user = self.user
        self.view.request = request

    def test_get_object(self):
        self.assertEqual(self.view.get_object(), self.user)

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), '/users/testuser/')



