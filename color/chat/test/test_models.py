from test_plus.test import TestCase

from chat.models import Message

class TestMessage(TestCase):

    def setUp(self):
        self.user = self.make_user('user1')
        self.other_user = self.make_user('user2')
        self.thi_user = self.make_user('user3')
        self.message = Message.objects.create(sender=self.user, recipient=self.other_user, message='你养我啊')
        self.response_mes = Message.objects. create(sender=self.other_user, recipient=self.user, message='那算了')
        Message.objects.create(sender=self.other_user, recipient=self.user, message='再发一条消息')
        self.message2 = Message.objects.create(sender=self.thi_user, recipient=self.user, message='复杂的sql')
        Message.objects.create(sender=self.thi_user, recipient=self.user, message='再来一条消息')

    def test___str__(self):
        assert self.message.__str__() == '你养我啊'

    def test_get_all_messages(self):
        assert Message.objects.get_all_messages(self.user, self.other_user).count()== 2

    def test_get_latest_message_user(self):

        Message.objects.create(sender=self.thi_user, recipient=self.user, message='最新消息')
        assert Message.objects.get_latest_message_user(self.user)== self.thi_user

    def test_get_conversation_userlist(self):
        res = Message.objects.get_conversation_userlist(self.user)
        print(res.query)










