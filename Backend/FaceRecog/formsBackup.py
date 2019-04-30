from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, TeacherTeachesSubject, StudentTookClass, SessionRecord, AttendanceRecord

from bootstrap_datepicker_plus import DateTimePickerInput


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields

class chooseSubject(forms.ModelForm):
    class Meta:
        model = TeacherTeachesSubject
        fields = ["subject"]

class createSession(forms.ModelForm):
    class Meta:
        model = SessionRecord
        fields = ["Teacher_Teaches_Subject","DateOfClass"]
        widgets = {
            'DateOfClass': 	DateTimePickerInput(), 
        }

class chooseSession(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ["session"]

class checkAttendanceOfSubject(forms.ModelForm):
    class Meta:
        model = StudentTookClass
        fields = ["Teacher_Teaches_Subject"]