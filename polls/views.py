from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from polls.repositories.question_repository import QuestionRepository
from polls.models import Choice
from django.views import generic
from polls.models import Question
from django.utils import timezone

# Class-based-views
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    def get_queryset(self):
        """Exclude any questions that aren't published yet."""
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

def vote(request, question_id):
    repo = QuestionRepository()
    try:
        question = repo.get_by_id(question_id)
    except Exception:
        raise Http404("Question does not exist")

    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse("polls:results", args=(question.id,))
        )