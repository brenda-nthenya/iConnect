from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import *
from django.core.mail import EmailMultiAlternatives
from django.http.response import Http404, HttpResponse
from django.db.models import Q
# Create your views here.

# Create your views here.
def register(request):
    if request.method=="POST":
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            user=form.save()
            profile.user=user
            profile.save()
        return redirect('login')
    else:
        form= UserRegisterForm()    
   
    params={
        'form':form,

    }
    return render(request, 'django_registration/registration_form.html', params)

def index(request):
    return render(request, 'index.html')

@login_required(login_url='login')
def home(request):
    all_profiles = Profile.objects.all()

    if request.method == "POST":
        query = request.POST.get('username')
        results = Profile.objects.filter(user__username=query)

        context = {
            'all_profiles': results,
        }

        return render(request, 'home.html', context)
    
    context = {
            'all_profiles': all_profiles,
        }

    return render(request, 'home.html', context)


def user_profile(request, username):
    user_prof = get_object_or_404(User, username=username)
    if request.user == user_prof:
        return redirect('profile', username=request.user.username)
    params = {
        'user_prof': user_prof,
    }
    return render(request, 'userprofile.html', params)

@login_required(login_url='login')
def profile(request, profile_id):
    user = get_object_or_404(User, pk=profile_id)

    can_update = False

    if request.user == user:
        can_update = True
    else:
        can_update = False

    context = {'user': user, 'can_update': can_update}
    return render(request, 'userprofile.html', context)

def update_profile(request):
    user = request.user
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        prof_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_form.is_valid() and prof_form.is_valid():
            user_form.save()
            prof_form.save()
            return redirect('profile', user.id)
    else:
        user_form = UserUpdateForm(instance=request.user)
        prof_form = UpdateProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'prof_form': prof_form
    }
    return render(request, 'update_profile.html', context )

class ListThreads(View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
        context = {
            'threads': threads
        }
        return render(request, 'social/inbox.html', context)

class CreateMessage(View):

    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
           
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get('message'),
            )
        message.save()
        return redirect('thread', pk=pk)

class CreateThread(View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()

        context = {
            'form': form
        }

        return render(request, 'social/create_thread.html', context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)

        username = request.POST.get('username')

        try:
            receiver = User.objects.get(username=username)
            if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
                thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
                return redirect('thread', pk=thread.pk)
            elif ThreadModel.objects.filter(user=receiver, receiver=request.user).exists():
                thread = ThreadModel.objects.filter(user=receiver, receiver=request.user)[0]
                return redirect('thread', pk=thread.pk)

            if form.is_valid():
                thread = ThreadModel(
                    user=request.user,
                    receiver=receiver
                )
                thread.save()

                return redirect('thread', pk=thread.pk)
        except:
            return redirect('create-thread')

class ThreadView(View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            'thread': thread,
            'form': form,
            'message_list': message_list
        }

        return render(request, 'social/thread.html', context)