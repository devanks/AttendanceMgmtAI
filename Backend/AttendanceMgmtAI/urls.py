"""AttendanceMgmtAI URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
 
urlpatterns = patterns('',
    # Examples:
 
    url(r'^face_detection/detect/$', 'face_detector.views.detect'),
 
    # url(r'^$', 'cv_api.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
 
    url(r'^admin/', include(admin.site.urls)),
)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from FaceRecog import views as FRView
from django.views.generic import TemplateView

import notifications.urls

# from rest_framework.documentation import include_docs_urls

urlpatterns = [
    url('', include('pwa.urls')),
    path('', FRView.HomePageView, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('accounts/signup/', FRView.SignUp.as_view(), name='signup'),
    path('accounts/', include('allauth.urls')),
    path('teacher_portal/', FRView.TeacherHomePageView, name= 'teacher_portal'),
    path('teacher_portal/session/uploadPhoto', FRView.UploadTestView, name= 'test_home'),
    path('teacher_portal/StudentsList', FRView.StudentTookClassList, name= 'StudentsList'),
    path('student_portal/', FRView.StudentHomePageView, name= 'student_portal'),
    path('student_portal/upload_photo', FRView.StudentUploadPhoto, name= 'uploadPhoto'),
    path('student_portal/check_attendance', FRView.StudentCheckAttendance, name= 'checkAttendance'),
    path('face_detection/detect/', FRView.detect, name='faceDetect'),
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    path('privacyPolicy/', TemplateView.as_view(template_name='privacyPolicy.html'), name= 'privacyPolicy'),
]
