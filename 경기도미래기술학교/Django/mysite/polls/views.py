from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils import timezone
from .models import Question, Dept
from .forms import QuestionForm

# Create your views here.
def index(request):
    question_list = Question.objects.order_by('-pub_date')
    result = [q.subject for q in question_list]
    
    # return HttpResponse(str(result))
    return render(request, 'polls/question_list.html', {'question_list': question_list})

def detail(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    context = { 'question': question }

    return render(request, 'polls/question_detail.html', context)

def answer_create(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question.answer_set.create(
        content=request.POST.get('content'), create_date=timezone.now()
    )

    return redirect('polls:detail', question_id=question_id)

def question_create(request):
    form = QuestionForm()
    
    return render(request, 'polls/question_form.html', {'form': form})

### form action 연습을 위한 페이지 작성
def data(request):
    age = request.GET.get('age')
    age2 = request.POST.get('age')

    return HttpResponse('%s %s' % (age, age2))

### DEPT Table
def form(request):

    return render(request, 'form.html')

def proc(request):
    deptno = request.GET.get('deptno')
    dname = request.GET.get('dname')
    loc = request.GET.get('loc')

    d = Dept(deptno=deptno, dname=dname, loc=loc)
    d.save()

    return HttpResponse('%s %s %s' % (deptno, dname, loc))