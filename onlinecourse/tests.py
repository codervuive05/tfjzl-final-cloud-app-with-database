from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Course, Enrollment, Question, Choice, Submission


class AssessmentFlowTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='learner', password='test-only')
        self.course = Course.objects.create(name='Python', description='Practice')
        Enrollment.objects.create(user=self.user, course=self.course)
        self.question = Question.objects.create(course=self.course, content='Select correct choices', grade=10)
        self.good = Choice.objects.create(question=self.question, content='Correct', is_correct=True)
        self.bad = Choice.objects.create(question=self.question, content='Incorrect')
        self.client.force_login(self.user)

    def test_extra_wrong_choice_prevents_credit(self):
        self.assertTrue(self.question.is_get_score([self.good.id]))
        self.assertFalse(self.question.is_get_score([self.good.id, self.bad.id]))
        self.assertFalse(self.question.is_get_score([]))

    def test_submission_result_and_course_template(self):
        detail = self.client.get(reverse('onlinecourse:course_details', args=[self.course.id]))
        self.assertContains(detail, 'Python')
        response = self.client.post(reverse('onlinecourse:submit', args=[self.course.id]),
                                    {'choice_1': str(self.good.id)}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['grade'], 10)
        self.assertEqual(response.context['possible'], 10)
        self.assertEqual(response.context['selected_ids'], [self.good.id])
        self.assertContains(response, 'Congratulations')
        self.client.force_login(User.objects.create_user(username='other', password='test-only'))
        submission = Submission.objects.get()
        denied = self.client.get(reverse('onlinecourse:exam_result', args=[self.course.id, submission.id]))
        self.assertEqual(denied.status_code, 404)
