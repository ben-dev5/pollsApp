import datetime
from django.test import TestCase
from django.utils import timezone
from polls.services.poll_service import PollService
from polls.repositories.question_repository import QuestionRepository
from django.urls import reverse



# Test pour gérer les dates du futur qui renvoie True malgré tout
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        service = PollService()
        future_question = service.create_question("Future question.", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    # foncion pour vérifier question trop anciennes
    def test_was_published_recently_with_old_question(self):
        service = PollService()
        old_question = service.create_question("Old question.", days=-2)
        self.assertIs(old_question.was_published_recently(), False)

    # fonction pour vérifier questions trop récentes
    def test_was_published_recently_with_recent_question(self):
        service = PollService()
        recent_question = service.create_question("Recent question.", days=0)
        recent_question.pub_date = timezone.now() - datetime.timedelta(hours=23)
        recent_question.save()
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    # message affiché quand aucune question disponible
    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context['latest_questions_list'], [])

    def test_past_question(self):
        service = PollService()
        question = service.create_question("Past question.", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_future_question(self):
        service = PollService()
        service.create_question("Future question.", days= 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_future_and_past_question(self):
        service = PollService()
        question = service.create_question("Past question.", days=-30)
        service.create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_two_past_questions(self):
        service = PollService()
        question1 = service.create_question("Past question 1.", days=-30)
        question2 = service.create_question("Past question 2.", days = -5)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question2, question1],
        )
class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        service = PollService()
        future_question = service.create_question("Future question.", days= 5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        service = PollService()
        past_question = service.create_question("Past Question.",days= -5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)