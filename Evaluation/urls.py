from django.contrib import admin
from django.urls import include, path
from . import views

from classroom.views import classroom, students, teachers

urlpatterns = [
    path('', include('classroom.urls')),
    path('', classroom.home, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/signup/', classroom.SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', students.StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/teacher/', teachers.TeacherSignUpView.as_view(), name='teacher_signup'),
]
