from django.shortcuts import render
from .models import Ticket
# Create your views here.
def ticket_list(request):
    ticket_lists = Ticket.objects.all()
    return render(request,'home.html')