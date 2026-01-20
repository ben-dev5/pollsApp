from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import Http404
from django.utils import timezone
from polls.services.poll_service import PollService

def index(request):
    service = PollService()
    latest_questions_list = service.get_latest_questions()
    return render(request, 'polls/index.html', {'latest_questions_list': latest_questions_list})

def detail(request, question_id):
    service = PollService()
    question = service.repo.get_by_id(question_id)
    if question.pub_date > timezone.now():
        raise Http404("Question not published yet")
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    service = PollService()
    question = service.repo.get_by_id(question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    service = PollService()
    choice_id = request.POST['choice']
    service.validate_and_vote(question_id, choice_id)
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
