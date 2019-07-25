from test_plus.test import TestCase
from django.urls import resolve, reverse

class TestUserUrls(TestCase):
    '''路由测试'''

    def setUp(self):
        self.user = self.make_user()

    def test_update_reverse(self):
        '''update路由反向解析'''
        self.assertEqual(self.reverse('users:update'), '/users/update/')

    def test_update_resolve(self):
        '''update路由正向解析'''
        self.assertEqual(resolve('/users/update/').view_name, 'users:update')

    def test_detail_reverse(self):
        self.assertEqual(reverse('users:detail', kwargs={"username":self.user.username}),'/users/testuser/' )

    def test_detail_resolve(self):
        self.assertEqual(resolve('/users/testuser/').view_name, 'users:detail')
