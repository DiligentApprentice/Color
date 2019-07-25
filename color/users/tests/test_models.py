from test_plus.test import TestCase

class TestUser(TestCase):
    '''用户模型测试'''

    def setUp(self):
        self.user = self.make_user()

    def test___str__(self):
        self.assertEqual(self.user.__str__(), 'testuser')

    def test_get_absolute_url(self):
        self.assertEqual(self.user.get_absolute_url(), '/users/testuser/')

    def test_get_nick_name(self):
        assert self.user.get_nick_name() == 'testuser'
        self.user.nick_name = '昵称'
        assert self.user.get_nick_name() == '昵称'
