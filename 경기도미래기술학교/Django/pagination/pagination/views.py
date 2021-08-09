from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.utils import timezone
from django.core.paginator import Paginator
from .models import *

# Create your views here.
def insert(request):
    for i in range(1, 123):  # 게시물 122개 추가
        data = Data(text='Data-%s' % i, cre_date=timezone.now())
        data.save()

    return HttpResponse('Insert Success')

def pagination(request):
    result = ''
    datas = Data.objects.order_by('id')
    p = Paginator(datas, 10)  # 한 페이지에 얼마만큼 출력할 것인지 파라미터 지정
    # result += '전체 데이터 수:  %s<br>' % p.count
    # result += '전체 페이지 수:  %s<hr>' % p.num_pages
    
    p = p.page(1)  # 조회를 원하는 페이지 파라미터 지정
    # list = str(p.object_list).replace('<', '&lt;').replace('>', '&gt;')
    # result += '현재 페이지 데이터:  %s<hr>' % list

    # result += '현재 페이지 데이터 시작번호: %s<br>' % p.start_index()
    # result += '현재 페이지 데이터 종료번호:  %s<hr>' % p.end_index()

    # result += '이전 페이지 존재유무: %s<br>' % p.has_previous()
    # if p.has_previous():
    #     result += '이전 페이지 번호: %s<br>' % p.previous_page_number()
    
    # result += '다음 페이지 존재유무: %s<br>' % p.has_next()
    # if p.has_next():
    #     result += '다음 페이지 번호: %s<br>' % p.next_page_number()
   
    return HttpResponse(result)
    # return render(request, 'templates/pagination.html')

def list(request):
    page = request.GET.get('page', '1')

    # if not page:
    #     page = 1

    # 조회
    datas = Data.objects.order_by('id')

    # 페이징 처리
    p = Paginator(datas, 10)  # 한 페이지에 출력되는 컬럼 갯수
    info = p.get_page(page)

    context = {
        'datas': info,
        'info': info
    }
    
    return render(request, 'list.html', context)