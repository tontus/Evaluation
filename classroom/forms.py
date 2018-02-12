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
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.reg_no = self.cleaned_data.get('reg_no')
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
