from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from classroom.models import Student, User, Answer


class StudentSignUpForm(UserCreationForm):
    reg_no = forms.IntegerField()

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        if not Student.objects.filter(reg_no=self.cleaned_data.get('reg_no')).exists():
            user = super().save(commit=False)
            user.is_student = True
            user.save()
            student = Student()
            student.user = user
            student.reg_no = self.cleaned_data.get('reg_no')
            student.save()
            # student = Student.objects.create(user=user)
            # student.reg_no = self.cleaned_data.get('reg_no')
            return user


class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user


class QuestionCreationForm(forms.Form):
    question = forms.CharField()
    model_answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'model_answer'}))
    marks = forms.IntegerField()
    students = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )


class TakeTestForm(forms.Form):
    answer = forms.CharField(widget=forms.Textarea(attrs={'class': 'answer'}))


class ScoreUpdateForm(forms.Form):
    answer_id = forms.IntegerField()
    given_score = forms.FloatField()
    CHOICES = [('1', 'Calculated Score'),
               ('2', 'Given Score')]

    final_score = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
