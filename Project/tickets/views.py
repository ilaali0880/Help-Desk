from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket
from .form import TicketForm, CommentForm, StatusForm, AssignForm
from .utils import is_agent


@login_required
def ticket_list(request):
    user_is_agent = is_agent(request.user)
    if user_is_agent:
        ticket_lists = Ticket.objects.all()
    else:
        ticket_lists = Ticket.objects.filter(requester=request.user)

    status = request.GET.get('status')
    if status:
        ticket_lists = ticket_lists.filter(status=status)

    q = request.GET.get('q')
    if q:
        ticket_lists = ticket_lists.filter(title__icontains=q)

    context = {
        'tickets': ticket_lists,
        'status_choices': Ticket.Status.choices,
        'is_agent': user_is_agent,
    }

    if request.GET.get('ajax'):
        return render(request, 'partials/ticket_list_partial.html', context)

    return render(request, 'home.html', context)


@login_required
def ticket_detail(request, id):
    ticket_details = get_object_or_404(Ticket, id=id)
    user_is_agent = is_agent(request.user)

    comment_form = CommentForm()
    status_form = StatusForm(instance=ticket_details) if user_is_agent else None
    assign_form = AssignForm(instance=ticket_details) if user_is_agent else None

    if request.method == 'POST':
        if 'comment_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.ticket = ticket_details
                comment.author = request.user
                comment.save()
                return redirect('detail', id=ticket_details.id)

        elif 'status_submit' in request.POST and user_is_agent:
            status_form = StatusForm(request.POST, instance=ticket_details)
            if status_form.is_valid():
                status_form.save()
                return redirect('detail', id=ticket_details.id)

        elif 'assign_submit' in request.POST and user_is_agent:
            assign_form = AssignForm(request.POST, instance=ticket_details)
            if assign_form.is_valid():
                assign_form.save()
                return redirect('detail', id=ticket_details.id)

    return render(request, 'detail.html', {
        'detail': ticket_details,
        'form': comment_form,
        'status_form': status_form,
        'assign_form': assign_form,
        'is_agent': user_is_agent,
    })


@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.requester = request.user
            ticket.save()
            return redirect('detail', id=ticket.id)
    else:
        form = TicketForm()
    return render(request, 'ticket_form.html', {'form': form})
@login_required
def dashboard(request):
    if not is_agent(request.user):
        return redirect('home')

    all_tickets = Ticket.objects.all()

    context = {
        'is_agent': True,
        'total': all_tickets.count(),
        'open_count': all_tickets.filter(status=Ticket.Status.OPEN).count(),
        'inprogress_count': all_tickets.filter(status=Ticket.Status.INPROGRESS).count(),
        'resolved_count': all_tickets.filter(status=Ticket.Status.RESOLVED).count(),
        'closed_count': all_tickets.filter(status=Ticket.Status.CLOSED).count(),
        'unassigned_count': all_tickets.filter(assigned_to__isnull=True).count(),
        'hardware_count': all_tickets.filter(category=Ticket.Category.HARDWARE).count(),
        'software_count': all_tickets.filter(category=Ticket.Category.SOFTWARE).count(),
        'network_count': all_tickets.filter(category=Ticket.Category.NETWORK).count(),
        'other_count': all_tickets.filter(category=Ticket.Category.OTHER).count(),
        'recent_tickets': all_tickets.order_by('-created_at')[:5],
    }
    return render(request, 'dashboard.html', context)