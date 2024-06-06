from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from polls.models import Poll, Participant, Type, Possibility
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import uuid
 
# Create your views here.

@login_required
def home(request):
    user_polls = Poll.objects.filter(user_id=request.user.id)
    print(user_polls)
    return render(request, 'home/index.html', {'user_polls' : user_polls})


# @login_required
# def create_polls(request):
#     return render(request, 'polls/edit-add.html')

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
@login_required
def manage_questions(request, id):
    if id not in [poll.id for poll in Poll.objects.filter(user=request.user)]:
        return redirect('home')
    
    return render(request, 'questions/manage_questions.html', {'current_poll': Poll.objects.filter(user=request.user, id=id).first(), 'types': Type.objects.all(), 'possibilities': Possibility.objects.all()})


# Share poll views
@login_required
def share_poll(request, id):
    shareLink = request.build_absolute_uri(reverse('polls.participant.link', args=[Poll.objects.get(id=id).token]))
    return JsonResponse({'title': Poll.objects.get(id=id).title, 'description': Poll.objects.get(id=id).description, 'link': shareLink})

def participant_login(request, token):
    if request.method == 'POST':
        email = request.POST['email']
        print(email) 
        poll = Poll.objects.filter(token=token).first()
        if not email:
            return render(request, 'participants/login.html', {'poll': Poll.objects.filter(token=token).first(), 'error': 'Email is required'})
        participant = Participant.objects.filter(poll=poll, email=email).first()
        if not participant:
            participant = Participant(poll=poll, email=email, token=uuid.uuid4())
            participant.save()
        return redirect(reverse('polls.respond', args=[poll.token, participant.token])) 
    
    return render(request, 'participants/login.html', {'poll': Poll.objects.filter(token=token).first()})

def generate_participant_link(request, token):
    poll = get_object_or_404(Poll, token=token)
    return redirect(reverse('polls.participants.login', args=[poll.token]))

def respond_poll(request, token, key):
    participant = Participant.objects.filter(token=key).first()
    if participant is None:
        return HttpResponse("Invalid participant") 
    return HttpResponse(f"Token poll: {token}, Participant: {Participant.objects.filter(token=key).first().email}")