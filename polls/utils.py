import csv
import uuid
from .models import Participant, Answer, QuestionPossibility
import re

def handle_uploaded_file(file, user):
    if file.name.endswith('.csv'):
        handle_csv_file(file, user)
    elif file.name.endswith('.txt'):
        handle_text_file(file, user)

def handle_csv_file(file, user):
    decoded_file = file.read().decode('utf-8').splitlines()
    reader = csv.DictReader(decoded_file)
    row2 = {}
    for row in reader:
        row2['last_name'] = row['nom']
        row2['first_name'] = row['prenoms']
        row2['email'] = row['email']
        row2['phone'] = row['tel']        
        create_participant(row2, user)
        
def handle_text_file(file, user):
    decoded_file = file.read().decode('utf-8')
    for line in decoded_file.splitlines():
        first_name, last_name, email, phone = line.split(',')
        row = {'first_name': first_name, 'last_name': last_name, 'email': email, 'phone': phone}
        create_participant(row, user)


def create_participant(row, user):
    first_name = row.get('first_name')
    last_name = row.get('last_name')
    email = row.get('email')
    phone = row.get('phone')

    Participant.objects.get_or_create(email=email, defaults={
        'user': user,
        'first_name': first_name,
        'last_name': last_name,
        'token': uuid.uuid4(),
        'phone': phone
    })

def extract_number(string):
    match = re.search(r'\d+', string)
    if match:
        return int(match.group())
    else:
        return None
    
    
def poll_questions_stats(poll):
    question_stats = []
    for question in poll.questions.all():
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
    return question_stats