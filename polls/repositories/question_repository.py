from polls.models import Question

class QuestionRepository:
    def get_latest(self, limit=5):
        return Question.objects.order_by("-pub_date")[:limit]

    def get_by_id(self, question_id):
        return Question.objects.get(pk=question_id)
