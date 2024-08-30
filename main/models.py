from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32, blank=True)
    age = models.IntegerField(default=18)
    gender = models.CharField(max_length=8, blank=True)
    email = models.CharField(max_length=32, blank=True)
    phonenumber = models.CharField(max_length=16, blank=True)

    def __str__(self):
        return self.user.username


class Progress(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.profile.user.username} {self.course.title} {self.lesson.title}"


class Lesson(models.Model):
    slug = models.SlugField(max_length=32)
    image = models.ImageField()
    title = models.CharField(max_length=100)
    content = models.TextField()
    video = models.CharField(max_length=32)
    note = models.TextField()

    def __str__(self):
        return self.title


class Course(models.Model):
    slug = models.SlugField(max_length=32)
    image = models.ImageField()
    title = models.CharField(max_length=100)
    lessons = models.ManyToManyField(Lesson)

    def __str__(self):
        return self.title
