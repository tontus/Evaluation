from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return HttpResponse('teachers:quiz_change_list')
        else:
            return redirect('students:quiz_list')
    return HttpResponse(request, 'classroom/home.html')