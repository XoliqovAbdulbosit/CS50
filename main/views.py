import markdown
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login as user_login, logout as user_logout, authenticate
from django.urls import reverse

from .models import Course, Lesson, Profile, Progress


# Create your views here.
def main(request):
    return render(request, 'home.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def registration(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user).save()
            user_login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration.html', {'errors': form.errors})
    return render(request, 'registration.html')


def logout(request):
    if request.method == 'POST':
        user_logout(request)
        return redirect('home')


def courses(request):
    courses = Course.objects.all()
    return render(request, 'courses.html', {'courses': courses})


def lesson(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)
    return render(request, 'lesson.html', {'course': course, 'lesson': lesson})


def note(request, course_slug, lesson_slug):
    note = Lesson.objects.get(slug=lesson_slug).note
    md = markdown.Markdown(extensions=['fenced_code'])
    note = md.convert(note)
    return render(request, 'note.html', {'note': note})


def completed(request, course_slug, lesson_slug):
    course = Course.objects.get(slug=course_slug)
    lesson = Lesson.objects.get(slug=lesson_slug)
    user = request.user
    progress = Progress.objects.get_or_create(profile=Profile.objects.get(user=user), course=course, lesson=lesson)
    if progress[1]:
        progress[0].save()
    return redirect(reverse('course', kwargs={'course_slug': course_slug}))


def profile(request):
    if request.method == 'POST':
        email = request.POST['email']
        gender = request.POST['gender']
        age = request.POST['age']
        phonenumber = request.POST['phonenumber']
        profile = Profile.objects.get(user=request.user)
        profile.email = email
        profile.gender = gender
        profile.age = age
        profile.phonenumber = phonenumber
        profile.save()
        return redirect('profile')
    profile = Profile.objects.get(user=request.user)
    dct = {}
    for course in Course.objects.all():
        progress = Progress.objects.filter(profile=Profile.objects.get(user=request.user), course=course).count()
        percentage = round(progress / course.lessons.count() * 100)
        dct[course.title] = percentage
    lst = [profile.email, profile.gender, profile.age, profile.phonenumber]
    return render(request, 'profile.html', {'lst': lst, 'dct': dct})


def course(request, course_slug):
    course = Course.objects.get(slug=course_slug)
    progress = Progress.objects.filter(profile=Profile.objects.get(user=request.user), course=course).count()
    percentage = round(progress / course.lessons.count() * 100)
    return render(request, 'course.html', {'course': course, 'percentage': percentage})
