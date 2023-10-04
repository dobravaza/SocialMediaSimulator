from django.shortcuts import render, redirect
from django.contrib .auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse



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

            pass
        else:
            messages.info(request, 'Hasła się nie zgadzają')
            return redirect("signup")

            # print("hasła się nie zgadzają")

    else:

        return render(request, 'signup.html')