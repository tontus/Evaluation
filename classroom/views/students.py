from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, get_list_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView, ListView
from django.shortcuts import get_object_or_404, render
from ..decorators import student_required
from django.contrib.auth.decorators import login_required

from ..forms import StudentSignUpForm, TakeTestForm
from ..models import User, Answer, Question, Student
from ..tasks import start_calculation


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
            messages.warning(self.request, 'This registration number is already registered.')
            return redirect('student_signup')


@method_decorator([login_required, student_required()], name='dispatch')
class QuestionList(ListView):
    template_name = 'classroom/students/questions.html'
    model = Question
    context_object_name = 'questions'

    def get_queryset(self):
        student = self.request.user.student
        queryset = Question.objects.exclude(answer_question__student=student)
        return queryset


@login_required
@student_required  # <-- here!
def take_test(request, pk):
    question = get_object_or_404(Question, pk=pk)
    student = request.user.student
    if Answer.objects.filter(student=student, question=question).exists():
        return redirect('students:questions')
    if request.method == 'POST':
        form = TakeTestForm(request.POST)
        if form.is_valid():
            answer = Answer()
            answer.student = student
            answer.question = question
            answer.text = form.cleaned_data['answer']
            answer.save()
            start_calculation.delay(answer.id)
            messages.success(request, 'The answer was submitted with success!')
            return redirect('students:questions')
    else:
        form = TakeTestForm()

        return render(request, 'classroom/students/take_test_form.html', {
            'question': question,
            'form': form,
        })
