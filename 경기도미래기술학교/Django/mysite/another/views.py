from django.shortcuts import render

# Create your views here.
def ad(request):
    # Kakao AdFit 광고 기능 시험 사용
    return render(request, 'another/ad.html')

def reply(request):
    # Disqus Comment 기능 시험 사용
    return render(request, 'another/reply.html')