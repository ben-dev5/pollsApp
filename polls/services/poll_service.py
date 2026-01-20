from polls.repositories.question_repository import QuestionRepository
from django.utils import timezone
import datetime

class PollService:
    def __init__(self):
        self.repo = QuestionRepository()

    def get_latest_polls(self):
        return self.repo.get_published_question()

    def get_latest_questions(self):
        return self.repo.get_latest()

    def get_by_id(self, question_id):
        return self.repo.get_by_id(question_id)

    def validate_and_vote(self, question_id, choice_id):
        question = self.repo.get_by_id(question_id)
        selected_choice = question.choice_set.get(pk=choice_id)
        selected_choice.votes += 1
        selected_choice.save()

        return selected_choice

    def create_question(self, text, days):
        pub_date = timezone.now() + datetime.timedelta(days=days)
        return self.repo.create_question(text, pub_date)