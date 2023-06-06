from django.views.generic import ListView
from assignments.models import UserAssignment, Assignment

class GradeListView(ListView):
    model = UserAssignment
    template_name = 'grades/list.html'
    context_object_name = 'user_assignments'

    def get_queryset(self):
        return super().get_queryset().select_related('assignment')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_assignments = context['user_assignments']
        assignment_ids = user_assignments.values_list('assignment_id', flat=True)
        assignments = Assignment.objects.filter(id__in=assignment_ids).select_related('course')
        context['assignments'] = assignments
        return context



