from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import GradeListView

urlpatterns = [ 
    path('', login_required(GradeListView.as_view()), name='assignment_list')
]