from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, TeacherTeachesSubject, StudentTookClass

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

class checkAttendanceOfSubject(forms.ModelForm):
    class Meta:
        model = StudentTookClass
        fields = ["Teacher_Teaches_Subject"]