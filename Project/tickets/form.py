
from django import forms
from .models import Ticket,Comment
from django.contrib.auth.models import User

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'priority', 'category']
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
class StatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
class AssignForm(forms.ModelForm):
    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.filter(groups__name='Agents'),
        required=False,
        label='تخصیص به'
    )

    class Meta:
        model = Ticket
        fields = ['assigned_to']