from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView

from classroom.models import Student, Answer


class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('teachers:questions')
        else:
            return redirect('students:questions')
    return redirect('login')


def leaderboard(request):
    data = []

    students = Student.objects.all()
    for student in students:
        total = 0
        total_marks = 0
        answers = Answer.objects.filter(student=student)
        temp = []
        answer_count = 0
        if answers.count() > 0:
            for answer in answers:
                full_marks = answer.question.marks
                final_score = answer.final_score
                if final_score >= 0:
                    answer_count += 1
                    total += final_score
                    total_marks += full_marks
            percentage = 0
            if total > 0 and total_marks > 0:
                percentage = total / total_marks * 100
            temp.append(student)
            temp.append(answer_count)
            temp.append(total)
            temp.append(round(percentage, 2))
            data.append(temp)
    data = sorted(data, key=lambda l: l[2], reverse=True)

    return render(request, 'classroom/leaderboard.html', {'data': data})
