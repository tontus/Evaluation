from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    reg_no = models.IntegerField(null=True, unique=True)

    def __str__(self):
        return str(self.reg_no)


class Question(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions')
    question = models.CharField(max_length=255)
    model_answer = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_question')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answer_student')
    text = models.TextField('Answer')
    calculated_score = models.FloatField(default=-1)
    given_score = models.FloatField(default=0)
    final_score = models.FloatField(default=-1)

    def __str__(self):
        return str(self.student.reg_no)
