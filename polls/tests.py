import datetime
from django.test import TestCase
from django.utils import timezone
from polls.services.poll_service import PollService
from polls.repositories.question_repository import QuestionRepository
from django.urls import reverse


# fonction pour faciliter la création de question réutilisable pour les tests
def create_question(question_text, days):
    repo = QuestionRepository()
    pub_date = timezone.now() + datetime.timedelta(days=days)
    return repo.create_question(question_text, pub_date)

# Test pour gérer les dates du futur qui renvoie True malgré tout
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        future_question = create_question("Future question.", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    # foncion pour vérifier question trop anciennes
    def test_was_published_recently_with_old_question(self):
        old_question = create_question("Old question.", days=-2)
        self.assertIs(old_question.was_published_recently(), False)

    # fonction pour vérifier questions trop récentes
    def test_was_published_recently_with_recent_question(self):
        recent_question = create_question("Recent question.", days=0)
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
        question = create_question("Past question.", -30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days= 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_questions_list"], [])

    def test_future_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question("Future question.", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_questions_list"],
            [question],
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
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
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)