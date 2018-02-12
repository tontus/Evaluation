from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import teachers

urlpatterns = [
    path('teachers/', include(([
                                   path('questions', teachers.QuestionList.as_view(), name='questions')
                               ], 'classroom'), namespace='teachers')),

]
urlpatterns += staticfiles_urlpatterns()
