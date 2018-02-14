from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import teachers, students

urlpatterns = [
    path('teachers/', include(([
                                   path('questions', teachers.questionList, name='questions'),
                                   path('add-question', teachers.QuestionCreateView.as_view(), name='add-question'),
                                   path('questions/<int:pk>/score', teachers.score, name='score'),
                               ], 'classroom'), namespace='teachers')),

    path('students/', include(([
                                   path('questions', students.QuestionList.as_view(), name='questions'),
                                   path('questions/<int:pk>/', students.take_test, name='take_test'),

                               ], 'classroom'), namespace='students')),

]
urlpatterns += staticfiles_urlpatterns()
