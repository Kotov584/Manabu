from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Assignment, UserAssignment
 
class AssignmentListView(ListView):
    model = UserAssignment
    template_name = 'assignments/assignment_list.html'
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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            file = form.cleaned_data['file'] 
            self.object.save()
            return self.form_valid(form)
        return self.form_invalid(form)

 
class AssignmentDetailView(DetailView):
    model = Assignment
    template_name = 'assignments/detail.html'
    context_object_name = 'assignment'
 
class AssignmentCreateView(CreateView):
    model = Assignment
    template_name = 'assignments/form.html'
    fields = ['title', 'content', 'courses', 'due_date', 'status']

class AssignmentUpdateView(UpdateView):
    model = UserAssignment
    template_name = 'assignments/detail.html'
    fields = ['title', 'content', 'courses', 'due_date', 'status']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AssignmentFileForm()
        return context

    def form_valid(self, form):
        file = form.cleaned_data['file'] 
        return super().form_valid(form)
 
class AssignmentDeleteView(DeleteView):
    model = Assignment
    template_name = 'assignments/confirm_delete.html'
    success_url = reverse_lazy('assignment_list')