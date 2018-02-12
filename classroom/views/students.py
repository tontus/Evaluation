from django.contrib.auth import login
from django.shortcuts import redirect, get_list_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView
from django.shortcuts import get_object_or_404, render
from ..decorators import student_required
from django.contrib.auth.decorators import login_required

from ..forms import StudentSignUpForm
from ..models import User, Answer, Question, Student


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')


@login_required
@student_required
def student_home_view(request, pk):
    answers = get_list_or_404(Answer, student__pk=pk)

    return render((request, 'classroom/students/home.html'), {
        'answers': answers
    })


@login_required
@student_required  # <-- here!
def give_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    student = request.user.student

    # body of the view...

    return render(request, 'classroom/students/give_answer_form.html', {
        'question': question
    })
