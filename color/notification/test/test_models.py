from test_plus.test import TestCase
from color.notification.models import Notification

class TestNotification(TestCase):
    '''通知模型测试用例'''

    def setUp(self):
        self.user = self.make_user('user1')
        self.other_user = self.make_user('user2')
        self.liker = Notification.objects.create(trigger=self.user,
                                                        recipient=self.other_user,
                                                        action='L',
                                                        )
        self.comment = Notification.objects.create(trigger=self.user,
                                                        recipient=self.other_user,
                                                        action='C',)

        self.reply = Notification.objects.create(trigger=self.user,
                                                   recipient=self.other_user,
                                                   action='R', )

    def test___str__(self):
        print(self.liker.__str__())
        assert self.liker.__str__() == 'user1点赞了'

    def test_get_notification_list(self):
        assert Notification.objects.get_notification_list(self.other_user).count() == 3

    def test_mark_all_notification_read(self):
        Notification.objects.mark_all_notification_read(self.other_user)
        assert Notification.objects.get_notification_list(self.other_user).count() == 0



