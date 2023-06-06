from django.urls import path
from .views import CourseListView, CourseDetailView
from django.contrib.auth.decorators import login_required

app_name = 'courses'

urlpatterns = [
    path('', login_required(CourseListView.as_view()), name='Course_list'),
    path('<int:pk>', login_required(CourseDetailView.as_view()), name='Course_detail'), 
]