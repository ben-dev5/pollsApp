from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from polls.repositories.question_repository import QuestionRepository
from polls.models import Choice

def index(request):
    repo = QuestionRepository()
    latest_question_list = repo.get_latest()
    context = {
        "latest_question_list": latest_question_list
    }
    return render(request, "polls/index.html", context)
def detail(request, question_id):
    repo = QuestionRepository()
    try:
        question = repo.get_by_id(question_id)
    except Exception:
        raise Http404("Question does not exist")
    return render(request, "polls/detail.html", {"question": question})
def results(request, question_id):
    repo = QuestionRepository()
    try:
        question = repo.get_by_id(question_id)
    except Exception:
        raise Http404("Question does not exist")
    return render(request, "polls/results.html", {"question": question})

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
