from test_plus.test import TestCase

from color.qa.models import Question, Answer, Vote

class TestQAmodels(TestCase):

    def setUp(self):
        self.user = self.make_user('user1')
        self.user2 = self.make_user('user2')
        self.user3 = self.make_user('user3')
        self.user4 = self.make_user('user4')
        self.questions = Question.objects.create(user=self.user,
                                  title='问题一',
                                  content='问题一内容')
        self.answer = Answer.objects.create(user=self.user2,
                                            content='问题一的回答',
                                            questions=self.questions,)
        self.vote = Vote.objects.create(user=self.user3,
                                        vote=self.questions)

    def test___str__(self):
        assert self.questions.__str__() == '问题一'

    def test_get_answer_num(self):
        init_num = self.questions.get_answer_num()
        Answer.objects.create(user=self.user3, content='问题一的第二条回答', questions=self.questions)
        assert self.questions.get_answer_num() == init_num+1

    def test_get_all_answers(self):
        assert self.answer in self.questions.get_all_answers()

    def test_get_vote_number(self):
        assert self.questions.get_vote_number() == 1
        Vote.objects.create(user=self.user4, value=False, vote= self.questions)
        assert self.questions.get_vote_number() == 0
        Vote.objects.create(user=self.user4, vote=self.answer)
        assert self.answer.get_vote_number() == 1

    def test_accept_answers(self):
        self.answer.accept_answers()
        assert self.answer.questions.q_type == 3
        assert self.answer.questions.is_solved == True
        assert self.questions in Question.objects.get_has_answer_questions()

    def test_get_null_answer_questions(self):
        question2 = Question.objects.create(user=self.user4,
                                            title='第二个问题',
                                            content='第二个问题内容')
        assert question2 in Question.objects.get_null_answer_questions()

    def test_get_upvoters(self):
        self.vote1 = Vote.objects.create(user=self.user3, value=True, vote=self.answer)
        assert self.user3 in  self.answer.get_upvoters()

    def test_get_downvoters(self):
        self.vote1 = Vote.objects.create(user=self.user4, value=False, vote=self.answer)
        assert self.user4 in  self.answer.get_downvoters()







