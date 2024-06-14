from django import forms
from polls.models import Participant

class QuestionForm(forms.Form):
    label = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'label',
            'placeholder': 'Entrer le libellé de la question'
        })
    )

    type = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={
            'id': 'question-type-select',
            'class': 'form-control',
        })
    )

    possibilities = forms.MultipleChoiceField(
        choices=[],
        widget=forms.SelectMultiple(attrs={
            'id': 'question-possibilities-select',
            'class': 'form-control',
        })
    )

    def __init__(self, *args, **kwargs):
        types = kwargs.pop('types', [])
        possibilities = kwargs.pop('possibilities', [])
        super(QuestionForm, self).__init__(*args, **kwargs)
        
        self.fields['type'].choices = [('', '--- Choisir l\'option de réponse ---')] + [(type.id, type.label) for type in types]
        self.fields['possibilities'].choices = [(possibility.id, possibility.label) for possibility in possibilities]

        self.fields['type'].widget.attrs.update({'choices': self.fields['type'].choices})
        self.fields['possibilities'].widget.attrs.update({'choices': self.fields['possibilities'].choices})
        

class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ['last_name', 'first_name', 'email', 'phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'first_name',
                'placeholder': 'Entrer votre prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'last_name',
                'placeholder': 'Entrer votre nom'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'id': 'email',
                'placeholder': 'Entrer votre adresse email'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'phone',
                'placeholder': 'Entrer votre numéro de téléphone'
            })
        }

        