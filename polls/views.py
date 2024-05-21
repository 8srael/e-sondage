from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from polls.models import Poll

# Create your views here.

@login_required
def home(request):
    user_polls = Poll.objects.filter(user_id=request.user.id)
    print(user_polls)
    return render(request, 'home/index.html', {'user_polls' : user_polls})


@login_required
def create_polls(request):
    return render(request, 'polls/edit-add.html')

@login_required
def store_polls(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        
        poll = Poll(title=title, description=description, user=request.user)
        poll.save()
        return redirect('home')
    else:
        return render(request, 'polls/edit-add.html')
