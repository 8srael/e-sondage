from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from polls.models import Poll
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@login_required
def home(request):
    user_polls = Poll.objects.filter(user_id=request.user.id)
    print(user_polls)
    return render(request, 'home/index.html', {'user_polls' : user_polls})


@login_required
def create_polls(request):
    return render(request, 'polls/edit-add.html')

# @login_required
# def store_polls(request):
#     if request.method == 'POST':
#         title = request.POST['title']
#         description = request.POST['description']
        
#         poll = Poll(title=title, description=description, user=request.user)
#         poll.save()
#         return redirect('home')
#     else:
#         return render(request, 'polls/edit-add.html')
   
    
@csrf_exempt
def store_polls(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        poll = Poll(title=title, description=description, user=request.user)
        poll.save()
        return JsonResponse({'message':'Data saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

# Questions views
def manage_questions(request, id):
    return render(request, 'questions/manage_questions.html', {'current_poll': Poll.objects.get(id=id)})