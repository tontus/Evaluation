from django.contrib import messages
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
    template_name = 'registration/signup_form_teacher.html'

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
class QuestionList(ListView):
    template_name = 'classroom/teachers/questions.html'
    model = Question


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionCreateView(CreateView):
    model = Question
    fields = ('question', 'model_answer', 'marks',)
    template_name = 'classroom/teachers/question_add_form.html'

    def form_valid(self, form):
        question = form.save(commit=False)
        question.owner = self.request.user
        question.save()
        messages.success(self.request, 'The quiz was created with success! Go ahead and add some questions now.')
        return redirect('teachers:questions')


