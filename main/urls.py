from django.urls import path
from . import views

urlpatterns = [
    path('', views.main, name='home'),
    path('login/', views.login, name='login'),
    path('registration/', views.registration, name='registration'),
    path('courses/', views.courses, name='courses'),
    path('logout/', views.logout, name='logout'),
    path('completed/<course_slug>/<lesson_slug>', views.completed, name='completed'),
    path('courses/<course_slug>/<lesson_slug>/note', views.note, name='note'),
    path('courses/<course_slug>/<lesson_slug>', views.lesson, name='lesson'),
    path('courses/<course_slug>', views.course, name='course'),
    path('profile/', views.profile, name='profile'),
]
