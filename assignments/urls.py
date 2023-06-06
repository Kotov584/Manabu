from django.urls import path
from .views import AssignmentListView, AssignmentDetailView, AssignmentCreateView, AssignmentUpdateView, AssignmentDeleteView
from django.contrib.auth.decorators import login_required

app_name = 'assignments'

urlpatterns = [
    path('', login_required(AssignmentListView.as_view()), name='assignment_list'),
    path('new/', login_required(AssignmentCreateView.as_view()), name='assignment_new'),
    path('<int:pk>/', login_required(AssignmentDetailView.as_view()), name='assignment_detail'),
    path('<int:pk>/edit/', login_required(AssignmentUpdateView.as_view()), name='assignment_edit'),
    path('<int:pk>/delete/', login_required(AssignmentDeleteView.as_view()), name='assignment_delete'),
]
