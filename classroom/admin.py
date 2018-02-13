from django.contrib import admin
from .models import Question,User,Student,Answer

# Register your models here.
admin.site.register(Question)
admin.site.register(User)
admin.site.register(Student)
admin.site.register(Answer)