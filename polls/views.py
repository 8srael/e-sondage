from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from .models import Poll, Participant, Type, Possibility, Question, QuestionPossibility, Answer
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import uuid
from .forms import ParticipantForm, UploadFileForm 
from .utils import  handle_uploaded_file, extract_number
from django.template.defaulttags import register


# Create your views here.
@login_required
def home(request):
    user_polls = Poll.objects.filter(user=request.user).order_by('-created_at')[:5]
    
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

@login_required
def polls(request):
    polls = Poll.objects.filter(user=request.user)
    return render(request, 'polls/index.html', {'polls': polls})
    

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
            else: # if no possibilities are selected, create a QuestionPossibility object with question and null possibility for free type question
                QuestionPossibility.objects.create(question=question)
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


def respond_poll(request, token, key):
    participant = get_object_or_404(Participant, token=key)
    poll = get_object_or_404(Poll, token=token)
    
    # recupérer les questions et les réponses deja enregistrées avant soumission
    questions = poll.questions.all()
    answers = Answer.objects.filter(participant=participant)
    
    answered_questions = {}
    for answer in answers:
        if not answer.question_possibility.possibility:
            answered_questions[answer.question_possibility.question.id] = answer.content
        else:
            if answer.question_possibility.question.id not in answered_questions.keys():
                answered_questions[answer.question_possibility.question.id] = [answer.question_possibility.possibility.id]
                print(answer.question_possibility)
            else:
                answered_questions[answer.question_possibility.question.id].append(answer.question_possibility.possibility.id)
                print(answer.question_possibility)         
    print('answered_questions :', answered_questions)
      
     # Trouver la première question non répondue
    first_unanswered_index = 1
    for index, question in enumerate(questions, start=1):
        if question.id not in answered_questions:
            first_unanswered_index = index
            break
    print('first_answered_index : ',first_unanswered_index)
    
    
    if request.method == 'POST':
        print(participant)
        participant.has_submitted = True
        participant.save()
        # print('in respond_poll method', request.POST.keys(), 'submitted' in request.POST.keys())
        return HttpResponse('<h2 style="text-align:center;">🙏🏽Merci pour votre participation🙏🏽</h2>')
    if participant.has_submitted:
        return HttpResponse('<h2 style="text-align:center;">⚠ Oups😅Vous avez déjà soumis vos réponses ⚠</h2>')
    return render(request, 'responses/questionnaire.html', {'poll': get_object_or_404(Poll, token=token), 'participant':  get_object_or_404(Participant, token=key), 'answered_questions': answered_questions, 'first_unanswered_index': first_unanswered_index})

@csrf_exempt
def save_one(request, token, key):
    if request.method == 'POST':
        print('in save_one method', request.POST.keys())
        poll = get_object_or_404(Poll, token=token)
        participant = get_object_or_404(Participant, token=key)
        for key in request.POST:
            if key.startswith('question'):
                question_id = extract_number(key)
                question = get_object_or_404(Question, id=question_id)
                values = request.POST.getlist(key)
                # values =  request.POST.getlist(key) if (question.type.label == 'Multiple') else request.POST.get(key)
                print(values) 
                
                if "libre" not in key:
                    Answer.objects.filter(participant=participant, question_possibility__question=question).delete()
                    for value in values:
                        question_possibility = get_object_or_404(QuestionPossibility, question=question, possibility=int(value))
                        print(question_possibility)
                        Answer.objects.create(question_possibility=question_possibility, participant=participant)
                else:
                    question_possibility = get_object_or_404(QuestionPossibility, question=question)
                    answer, created = Answer.objects.get_or_create(participant=participant, question_possibility=question_possibility, defaults={'content': values[0]})
                   
                    if not created:
                       answer.content = values[0]
                       answer.save()
                # if "libre" not in key:
                #     for value in values:
                #         question_possibility = get_object_or_404(QuestionPossibility, question=question, possibility=int(value))
                #         print(question_possibility)
                #         Answer.objects.create(question_possibility=question_possibility, participant=participant)
                # else:
                #     question_possibility = get_object_or_404(QuestionPossibility, question=question)
                #     print(question_possibility)
                #     Answer.objects.create(participant=participant, question_possibility=question_possibility, content=values[0])
        return JsonResponse({'status':'Saved successfully'}, status=200)
    else:
        return JsonResponse({'status':'Invalid request'}, status=400)
    
# custom template tags
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# def pList(request):
#     return render(request, 'participants/list.html', {'participants': Participant.objects.all()}

# statistics views
def stats(request):
    polls = Poll.objects.filter(user=request.user)
    selected_poll = Poll.objects.latest('created_at')   
    return render(request, 'statistics/index.html', {
        'polls': polls,
        'selected_poll': selected_poll,
    })
    
def stats_data(request, id):
    polls = Poll.objects.filter(user=request.user)
    selected_poll = get_object_or_404(Poll, id=id)
    questions = selected_poll.questions.all()
    question_stats = []
    
    for question in questions:
        stats = {'question': question.label, 'type': question.type.label, 'responses': {}}
        
        if question.type.label == 'Libre':
            answers = Answer.objects.filter(question_possibility__question=question)
            stats['responses'] = [answer.content for answer in answers]
        else:
            possibilities = QuestionPossibility.objects.filter(question=question)
            for possibility in possibilities:
                label = possibility.possibility.label if possibility.possibility else 'None'
                stats['responses'][label] = Answer.objects.filter(question_possibility=possibility).count()
        
        question_stats.append(stats) 
        
    print(len(question_stats))
        
    return JsonResponse({
        'poll': {'title': selected_poll.title, 'description': selected_poll.description},
        'question_stats': question_stats,
    })       
    # return render(request, 'statistics/index.html', {
    #     'polls': polls,
    #     'selected_poll': selected_poll,
    #     'question_stats': question_stats,
    # })