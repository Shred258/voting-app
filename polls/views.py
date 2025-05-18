from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .forms import CustomUserCreationForm
from .models import Poll, Choice, Vote

def home(request):
    return render(request, 'polls/home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {username}!")
            return redirect('poll_list')
        else:
            messages.error(request, "Invalid username or password")
    return render(request, 'polls/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('poll_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'polls/register.html', {'form': form})

@login_required
def poll_list(request):
    now = timezone.now()
    polls = Poll.objects.filter(closes_at__gt=now, is_closed=False)
    return render(request, 'polls/poll_list.html', {'polls': polls})



@login_required
def poll_list(request):
    now = timezone.now()
    polls = Poll.objects.filter(closes_at__gt=now, is_closed=False)
    return render(request, 'polls/poll_list.html', {'polls': polls})

@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    
    if poll.is_closed or poll.closes_at < timezone.now():
        poll.is_closed = True
        poll.save()
        return redirect('results', poll_id=poll.id)
    
    if Vote.objects.filter(user=request.user, poll=poll).exists():
        messages.warning(request, "You have already voted in this poll!")
        return redirect('poll_list')
    
    if request.method == 'POST':
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = Choice.objects.get(pk=choice_id)
            choice.votes += 1
            choice.save()
            Vote.objects.create(user=request.user, poll=poll, choice=choice)
            messages.success(request, "Vote recorded successfully!")
            return redirect('poll_list')
    
    choices = Choice.objects.filter(poll=poll)
    return render(request, 'polls/vote.html', {
        'poll': poll,
        'choices': choices,
        'hide_results': True
    })

@login_required
def results(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choices = Choice.objects.filter(poll=poll).order_by('-votes')
    
    # Allow admin to see results anytime
    if not poll.is_closed and poll.closes_at > timezone.now() and not request.user.is_admin:
        return redirect('poll_list')
    
    return render(request, 'polls/results.html', {
        'poll': poll,
        'choices': choices,
        'show_admin_stats': request.user.is_admin  # Pass admin flag to template
    })