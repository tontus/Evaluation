from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.views.generic.base import View

from classroom.decorators import teacher_required
from classroom.forms import TeacherSignUpForm, ScoreUpdateForm
from classroom.models import User, Question, Answer


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
    context_object_name = 'questions'

    def get_queryset(self):
        teacher = self.request.user
        queryset = Question.objects.filter(owner=teacher)
        return queryset


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


def score(request, pk):

    if request.method == 'POST':
        form = ScoreUpdateForm(request.POST)

        if form.is_valid():
            answer_id = form.cleaned_data['answer_id']
            answer = Answer.objects.get(id=answer_id)
            answer.given_score = form.cleaned_data['given_score']
            choice = form.cleaned_data['final_score']

            if choice is '2':
                answer.final_score = answer.given_score
            elif choice == '1':
                answer.final_score = answer.calculated_score
            answer.save()

    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    forms = []
    for answer in answers:
        data = {
            'answer_id': answer.id,
            'given_score': answer.given_score
        }
        form = ScoreUpdateForm(data)
        forms.append(form)

    lists = zip(answers, forms)
    return render(request, 'classroom/teachers/score.html', {
        'question': question,
        'answers': answers,
        'list': lists,
        
    })
