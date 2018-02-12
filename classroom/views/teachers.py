from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from classroom.decorators import teacher_required
from classroom.forms import TeacherSignUpForm
from classroom.models import User, Question


class TeacherSignUpView(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'registration/signup_form.html'
    kkk = "asdfa"

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:questions')

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class
    #     return render(request, self.template_name, {'form': form})


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionList(View):
    template_name = 'classroom/teachers/questions.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
