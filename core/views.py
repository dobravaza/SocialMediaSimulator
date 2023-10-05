from django.shortcuts import render, redirect
from django.contrib .auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import  login_required
from .models import Profile


@login_required(login_url='signin')
def index(request):
    return render(request, 'index.html')

def signup(request):

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Mail zajęty')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Nazwa użytkownika zajęta.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                user_login = auth.authenticate(username=username, password=password)
                auth.login(request,user_login)


                #tworzenie profilu uztkownika
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('./settings')
            pass
        else:
            messages.info(request, 'Hasła się nie zgadzają')
            return redirect("./signup")

            # print("hasła się nie zgadzają")

    else:

        return render(request, './signup.html')

@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, './setting.html', {'user_profile':user_profile})

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('./')
        else:
            messages.info(request, 'Wprowadzono nie poprawne dane.')
            return redirect('./signin')
    else:

        return render(request, './signin.html')

@login_required(login_url='signin')

def logout(request):
    auth.logout(request)
    return redirect('./signin')