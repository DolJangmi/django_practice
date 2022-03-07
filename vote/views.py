from django.shortcuts import render, redirect
from .models import Topic, Choice
from django.utils import timezone

# Create your views here.
def index(request):
    t = Topic.objects.all()
    t = t.order_by("-pubdate")
    context = {
        'tset': t
    }
    return render(request, 'vote/index.html', context)

def detail(request, vpk):
    t = Topic.objects.get(id=vpk)
    c = t.choice_set.all()
    context = {
        't': t,
        'cset': c
    }
    return render(request, 'vote/detail.html', context)

def vote(request, vpk):
    t = Topic.objects.get(id=vpk)
    if not request.user in t.voter.all():
        # 토픽에 투표하지 않은 사람들만 종속문장 실행
        t.voter.add(request.user)
        
        cpk = request.POST.get('ch')
        c = Choice.objects.get(id=cpk)
        c.choicer.add(request.user)
    return redirect('vote:detail', vpk)

def cancel(request, vpk):
    t = Topic.objects.get(id=vpk)
    u = request.user
    if u in t.voter.all():
        t.voter.remove(u)
        u.choice_set.get(topic=t).choicer.remove(u) # 유저가 고른 초이스중에 topic이 t인 레코드중에 초이서에서 u를 remove
    return redirect('vote:detail', vpk)

def create(request):
    if request.method == 'POST':
        s = request.POST.get('sub')
        c = request.POST.get('con')

        names = request.POST.getlist('chname')
        files = request.FILES.getlist('chpic')
        comms = request.POST.getlist('chcom')
        if len(names) > 1:
            t = Topic(subject = s, maker = request.user, content = c, pubdate = timezone.now())
            t.save()

            for i, j ,k in zip(names, files, comms):
                Choice(topic = t, chname = i, chpic = j, chcom = k).save()
            return redirect('vote:index')
    return render(request, 'vote/create.html')