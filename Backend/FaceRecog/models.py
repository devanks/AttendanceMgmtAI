# users/models.py
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator

class CustomUserManager(UserManager):
    pass

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    # add additional fields in here
    # isTeacher = model.BooleanField(default='0')
    def __str__(self):
        return self.username

year_and_semester = (
    ("FrY1", "First Year, First Semester"),
    ("FrY2", "First Year, Second Semester"), 
    ("SeY1", "Second Year, First Semester"), 
    ("SeY2", "Second Year, Second Semester"), 
    ("ThY1", "Third Year, First Semester"), 
    ("ThY2",  "Third Year, Second Semester"), 
    ("FoY1", "Fourth Year, First Semester"),
    ("FoY2", "Fourth Year, Second Semester"), 
    ("FiY1", "Fifth Year, First Semester"),
    ("FiY2", "Fifth Year, Second Semester"),
    ("XYRp", "Repeater"),
)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    rollNumber = models.CharField(max_length=9,unique=True)
    year = models.CharField(max_length=4) #add validator for year
    presentSemester = models.CharField(max_length=4,choices=year_and_semester,default="FrY1")
    def __str__(self):
        return self.rollNumber


class Subject(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=6) #Add subject code validator
    faceData = models.BinaryField()
    def __str__(self):
        return self.name

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    subjects = models.ManyToManyField(Subject, through='TeacherTeachesSubject', through_fields=('teacher', 'subject'),)
    def __str__(self):
        return self.user.username

class TeacherTeachesSubject(models.Model):
    teacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    classroom = models.CharField(max_length=8)
    students = models.ManyToManyField(Student, through='StudentTookClass', through_fields=('Teacher_Teaches_Subject', 'student'),)
    verbose_name = "Subject taught by Teacher"
    verbose_name_plural = "Subjects taught by different Teachers"
    def __str__(self):
        return self.teacher.user.username

class StudentTookClass(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    Teacher_Teaches_Subject = models.ForeignKey(TeacherTeachesSubject,on_delete=models.CASCADE)
    presentAttendance = models.IntegerField(default=0, validators=[MaxValueValidator(100), MinValueValidator(0)]) #automate value each time record added to attendance
    # attendance = models.ManyToManyField(Subject, through='StudentTookClass', through_fields=('student', 'Teacher_Teaches_Subject'),)
    verbose_name = "Class taken by student"
    verbose_name_plural = "Classes taken by different students"
    def __str__(self):
        return self.student.rollNumber
    

class AttendanceRecord(models.Model):
    attendance = models.ManyToManyField(StudentTookClass)
    DateOfClass = models.DateField(auto_now_add=True)
    isPresent = models.BooleanField()
    # def __str__(self):
        # return self.attendance.student.user.username






