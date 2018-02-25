from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_teacher:
                return redirect('teachers:questions')
            if user.is_student:
                return redirect('students:questions')
        else:
            messages.error(request, "Enter Correct Username and password!")
            return render(request, 'registration/login.html', {'form': form})
    else:

        return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})
