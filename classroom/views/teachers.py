import csv

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


# @method_decorator([login_required, teacher_required], name='dispatch')
# class QuestionList(ListView):
#     template_name = 'classroom/teachers/questions.html'
#     model = Question
#     context_object_name = 'questions'
#
#     def get_queryset(self):
#         teacher = self.request.user
#         queryset = Question.objects.filter(owner=teacher)
#         return queryset

@teacher_required()
@login_required()
def questionList(request):
    answer_counts = []
    teacher = request.user
    questions = Question.objects.filter(owner=teacher)
    for question in questions:
        answer_count = Answer.objects.filter(question=question).count()
        answer_counts.append(answer_count)
    infos = zip(questions, answer_counts)

    return render(request, 'classroom/teachers/questions.html', {
        'infos': infos,
    })


@method_decorator([login_required, teacher_required], name='dispatch')
class QuestionCreateView(CreateView):
    model = Question
    fields = ('question', 'model_answer', 'marks',)
    template_name = 'classroom/teachers/question_add_form.html'

    def form_valid(self, form):
        question = form.save(commit=False)
        question.owner = self.request.user
        question.save()
        messages.success(self.request, 'The question was created with success!')
        return redirect('teachers:questions')


@login_required()
@teacher_required()
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
            if answer.final_score > answer.question.marks:
                messages.error(request, 'Final score can not be bigger than total marks '+str(answer.question.marks)+'!')
            else:
                answer.save()

    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question)
    forms = []
    for answer in answers:
        if answer.final_score == answer.calculated_score:
            data = {
                'answer_id': answer.id,
                'given_score': answer.given_score,
                'final_score': '1'
            }
        else:
            data = {
                'answer_id': answer.id,
                'given_score': answer.given_score,
                'final_score': '2'
            }
        form = ScoreUpdateForm(data)
        forms.append(form)

    lists = zip(answers, forms)
    list_count = answers.count()
    return render(request, 'classroom/teachers/score.html', {
        'question': question,
        'answers': answers,
        'list': lists,
        'list_count': list_count

    })


@login_required()
@teacher_required()
def csv_download(request, pk):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="log.csv"'

    writer = csv.writer(response)
    log = Answer.objects.filter(question_id=pk)
    question = Question.objects.get(id=pk)
    writer.writerow(['Question:',question.question,'Marks:',question.marks])
    writer.writerow(['Model Answer:',question.model_answer])
    writer.writerow(['Registration Number', 'Answer', 'Calculated Score', 'Given Score', 'Final Score'])
    for data in log:
        writer.writerow([data.student.reg_no, data.text, data.calculated_score, data.given_score, data.final_score])

    return response
