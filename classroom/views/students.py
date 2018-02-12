from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, get_list_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django.shortcuts import get_object_or_404, render
from ..decorators import student_required
from django.contrib.auth.decorators import login_required

from ..forms import StudentSignUpForm
from ..models import User, Answer, Question, Student


class StudentSignUpView(CreateView):
    model = User
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form_student.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        try:
            user = form.save()
            login(self.request, user)
            return redirect('students:questions')
        except AttributeError:
            messages.error(self.request, 'This registration number is already registered.')
            return redirect('student_signup')


@method_decorator([login_required, student_required()], name='dispatch')
class QuestionList(ListView):
    template_name = 'classroom/students/questions.html'
    model = Question


@login_required
@student_required  # <-- here!
def give_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    student = request.user.student

    # body of the view...

    return render(request, 'classroom/students/give_answer_form.html', {
        'question': question
    })
