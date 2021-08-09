from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.utils import timezone
from .models import Question, Dept
from .forms import QuestionForm, AnswerForm

# Create your views here.
def index(request):
    page = request.GET.get('page', '1')  # 페이지 등록

    # 페이지 조회
    question_list = Question.objects.order_by('pub_date')
    # result = [q.subject for q in question_list]

    # 페이징 처리
    paginator = Paginator(question_list, 10)  # 한 페이지에 10개 컬럼 출력
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj}
    
    # return HttpResponse(str(result))
    # return render(request, 'polls/question_list.html', {'question_list': question_list})
    return render(request, 'polls/question_list.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}

    return render(request, 'polls/question_detail.html', context)

def answer_create(request, question_id):
    # 방법1
    # question = get_object_or_404(Question, pk=question_id)
    # question.answer_set.create(
    #     content=request.POST.get('content'), create_date=timezone.now()
    # )

    # 방법2
    # a = Answer(content=request.POST.get('content'), create_date=timezone.now(), question=question)
    # a.save()

    # 방법3
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            
            return redirect('polls:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question': question, 'form': form}

    return render(request, 'polls/question_detail.html', context)

### `question_create` 함수에 데이터를 저장하는 코드 수정 전
# def question_create(request):
#     form = QuestionForm()
    
#     return render(request, 'polls/question_form.html', {'form': form})

### `question_create` 함수에 데이터를 저장하는 코드 수정 후
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.pub_date = timezone.now()
            question.save()
            return redirect('polls:index')
    else:
        form = QuestionForm()
    context = {'form': form}

    return render(request, 'polls/question_form.html', context)

### form action 연습을 위한 페이지 작성
def data(request):
    age = request.GET.get('age')
    age2 = request.GET.get('age')

    return HttpResponse('%s %s' % (age, age2))

### python - DEPT Table DB Loading
def form(request):

    return render(request, 'form.html')

def proc(request):
    dname = request.GET.get('dname')
    deptno = request.GET.get('deptno')
    loc = request.GET.get('loc')

    d = Dept(dname=dname, deptno=deptno, loc=loc)
    d.save()

    return HttpResponse('%s %s %s' % (dname, deptno, loc))