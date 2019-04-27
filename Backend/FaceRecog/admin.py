from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Student, Subject, Teacher, TeacherTeachesSubject, StudentTookClass, AttendanceRecord

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    search_fields = ['username','first_name','last_name']

class CustomStudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ('user', 'rollNumber', 'year','presentSemester')
    search_fields = ['user__username','user__first_name','user__last_name','year','rollNumber']

class CustomSubjectAdmin(admin.ModelAdmin):
    model = Subject
    list_display = ('name', 'code')
    search_fields = ['name','code']


class CustomTeacherAdmin(admin.ModelAdmin):
    model = Teacher
    search_fields = ['user__username','user__first_name','user__last_name']

class CustomTeacherTeachesSubjectAdmin(admin.ModelAdmin):
    model = TeacherTeachesSubject
    list_display = ('teacher', 'subject', 'classroom')
    search_fields = ['teacher__user__username','teacher__user__first_name','subject__name',]

class CustomStudentTookClassAdmin(admin.ModelAdmin):
    model = StudentTookClass
    list_display = ('student', 'Teacher_Teaches_Subject', 'presentAttendance')

class CustomAttendanceRecordAdmin(admin.ModelAdmin):
    model = AttendanceRecord
    list_display = ('student', 'session', 'isPresent')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student, CustomStudentAdmin)
admin.site.register(Subject, CustomSubjectAdmin)
admin.site.register(Teacher, CustomTeacherAdmin)
admin.site.register(TeacherTeachesSubject,CustomTeacherTeachesSubjectAdmin)
admin.site.register(StudentTookClass, CustomStudentTookClassAdmin)
admin.site.register(AttendanceRecord, CustomAttendanceRecordAdmin)
