from polls.models import Question
from django.utils import timezone

class QuestionRepository:
    def get_latest(self, limit=5):
        return  Question.objects .filter(pub_date__lte=timezone.now()) .order_by("-pub_date")[:5]

    def get_published_questions(self):
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

    def get_by_id(self, question_id):
        return Question.objects.get(pk=question_id)

    def create_question(self, text, pub_date):
        return Question.objects.create(question_text=text, pub_date=pub_date)