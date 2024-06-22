from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Poll, Participant, Type, Possibility, Question, QuestionPossibility
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import uuid
from .forms import ParticipantForm, UploadFileForm 
from .utils import  handle_uploaded_file


# Create your views here.
@login_required
def home(request):
    user_polls = Poll.objects.filter(user_id=request.user.id)
    participants_polls = Participant.objects.filter(user=request.user)
    return render(request, 'home/index.html', {'user_polls' : user_polls, 'participants_polls': participants_polls})


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
# @login_required
# def manage_questions(request, id):
#     if id not in [poll.id for poll in Poll.objects.filter(user=request.user)]:
#         return redirect('home')
#     if request.method == 'POST':
#         print(request.POST.get('label'), request.POST.get('type'),)
#         form = QuestionForm(request.POST)
#         # if form.is_valid():
#         #     label = form.cleaned_data['label']
#         #     type_id = form.cleaned_data['type']
#         #     possibilities = form.cleaned_data['possibilities']
#         #     poll = Poll.objects.get(id=id)
#         #     question = Question(label=label, type_id=type_id)
#         #     question.save()
#         #     question.possibilities.set(possibilities)
#         #     poll.questions.add(question)
            
#             # return redirect('polls.questions.manage', {'id':id, 'message': 'Question enregistrée avec succès'})
#     else:
#         print('no valid')
#         form = QuestionForm(types=Type.objects.all(), possibilities=Possibility.objects.all())
# 
#   return render(request, 'questions/manage_questions.html', {'current_poll': Poll.objects.filter(user=request.user, id=id).first(), 'form':form})


@login_required
def manage_questions(request, id):
    if id not in [poll.id for poll in Poll.objects.filter(user=request.user)]:
        return redirect('home')
    if request.method == 'POST':
        label = request.POST.get('label')
        type_id = request.POST.get('type')
        possibilities = request.POST.get('possibilities')
        poll = Poll.objects.get(id=id)

        if label and type_id:
            question = Question(label=label, type_id=type_id)
            question.save()
            if possibilities:
                possibilities = [int(possibility) for possibility in possibilities.split(',')]
                question.possibilities.set(possibilities)
            poll.questions.add(question)          
            
            return redirect('polls.questions.manage', id=id)
        
    return render(request, 'questions/manage_questions.html', {'current_poll': Poll.objects.filter(user=request.user, id=id).first(), 'types': Type.objects.all(), 'possibilities': Possibility.objects.all()})

# Possibilities json response
@csrf_exempt
def possibilities(request):
    if request.method == 'POST':
        lab = request.POST.get('lab')
        possibility = Possibility(label=lab)        
        possibility.save()
        return JsonResponse({'message':'Data saved successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
# participants views
def participants(request):
    participants = Participant.objects.filter(user=request.user)
    form = ParticipantForm()
    file_form = UploadFileForm()
    if request.method == 'POST':
        if 'manual' in request.POST.keys():
            form = ParticipantForm(request.POST) 
            if form.is_valid():
                print('here')
                participant = form.save(commit=False)
                participant.user = request.user
                participant.token = uuid.uuid4()
                participant.save()
                return redirect('participants.index')
        if 'import' in request.POST.keys(): 
            file_form = UploadFileForm(request.POST, request.FILES)
            if file_form.is_valid():
                handle_uploaded_file(request.FILES['fichier'], request.user)
                return redirect('participants.index')     
    return render(request, 'participants/index.html', {'form': form, 'participants': participants, 'file_form' : file_form})

def participant_delete(request, id):
    participant = get_object_or_404(Participant, id=id)
    participant.delete()    
    return redirect('participants.index')
    

# Share poll views
@login_required
def share_poll(request, id):
    participants = Participant.objects.filter(user=request.user)
    informations = []
    for participant in participants:
        informations.append({
            'full_name': f"{participant.last_name} {participant.first_name}",
            'email': participant.email,
            'link': request.build_absolute_uri(reverse('polls.respond', args=[Poll.objects.get(id=id).token, participant.token])),
            'submitted': participant.has_submitted
        })
    # print(informations)
    return render(request, 'participants/share.html', {'poll': Poll.objects.get(id=id), 'informations': informations})
# @login_required
# def share_poll(request, id):
#     shareLink = request.build_absolute_uri(reverse('polls.participants.link', args=[Poll.objects.get(id=id).token]))
#     return JsonResponse({'title': Poll.objects.get(id=id).title, 'description': Poll.objects.get(id=id).description, 'link': shareLink})


def respond_poll(request, token, key):
    poll = get_object_or_404(Poll, token=token)
    participant = get_object_or_404(Participant, token=key)
    return render(request, 'responses/questionnaire.html', {'poll': get_object_or_404(Poll, token=token), 'participant': participant})

@csrf_exempt
def save_one(request, token, key):
    print(request.method)
    if request.method == 'POST':
        poll = get_object_or_404(Poll, token=token)
        participant = get_object_or_404(Participant, token=key)
        print(request.POST.keys())
        return JsonResponse({'status':'Data saved successfully'}, status=200)
    else:
        return JsonResponse({'status':'Invalid request'}, status=400)