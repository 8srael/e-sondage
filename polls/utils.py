import csv
import uuid
from .models import Participant

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