from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from polls.repositories.question_repository import QuestionRepository
from polls.models import Choice
from django.views import generic
from polls.models import Question

class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        repo = QuestionRepository()
        return repo.get_latest()

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

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