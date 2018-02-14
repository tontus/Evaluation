import logging

from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from Evaluation.celery import app
from .models import Answer
from .calculate import Calculate


@app.task
def start_calculation(answer_id):
    calculate = Calculate()
    answer = Answer.objects.get(id=answer_id)
    answer.calculated_score = float("{0:.2f}".format(
        calculate.similarity(answer.question.model_answer, answer.text, True) * answer.question.marks))
    if answer.final_score == -1:
        answer.final_score = answer.calculated_score
    answer.save()

