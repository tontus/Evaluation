from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from classroom.models import Student, User


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
    interests = forms.ModelMultipleChoiceField(
        queryset=Student.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
