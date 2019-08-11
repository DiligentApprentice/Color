from test_plus.test import CBVTestCase
from django.test import RequestFactory

from color.qa.models import Question, Answer, Vote
from color.qa import views
class BaseQATestCase(CBVTestCase):

    def setUp(self):
        self.user1 = self.make_user('user1')
        self.user2 = self.make_user('user2')
        self.request = RequestFactory().get('index/')
        self.q1 = Question(user=self.user1, title='问题一', content='内容一')
        self.q2 = Question(user=self.user2, title='问题二', content='内容二')
        self.answer = Answer(user=self.user2, content='问题一的回答', questions=self.q1)


class QATest(BaseQATestCase):

    def test_get_context_data(self):
        self.request.user = self.user1
        response = self.get(views.QAListView, request=self.request)
        print(response.context_data['questions'])
        print(response.context)
        assert response.status_code == 200
        self.assertContext('active', 'all')
        # self.assertQuerysetEqual(response.context_data['questions'], map(repr, [self.q1, self.q2]), ordered=False)







