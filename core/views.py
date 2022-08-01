from django.shortcuts import render,redirect 
from django.http import HttpResponse
from django.contrib.auth.models import User, auth 
from django .contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    template_name = 'index.html'
    return render(request, template_name)


def signup(request):
    template_name = 'signup.html'
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, "email already exits")
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, "sorry, username is taken up")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password2)
                user.save()
            
                # create a profile 
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()

                # TODO log user in and also redirect them to setting page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                return redirect("settings")


        else:
            message = "Sorry, passwords dont match"
            messages.info(request, message)
            return redirect('signup')

    else:
        return render(request, template_name)


def login(request):
    template_name = 'signin.html'
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password'] 

        user = auth.authenticate(username=username, password=password)
        if user is not None: 
            auth.login(request,user)
            return redirect('index')
        else: 
            messages.info(request,"Credentials Invalid")
            return redirect('login')
    else:
        return render(request, template_name)

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def settings(request):
    template_name = 'setting.html'
    user_profile = Profile.objects.get(user=request.user)
    if request.method == "POST": 
        if request.FILES.get('image') == None:
            image = user_profile.profile_image
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profile_image = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            
        return redirect('settings')
    return render(request, template_name, {'user_profile':user_profile})