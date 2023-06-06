from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from courses.models import Course

@login_required
def index(request):
    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'dashboard/index.html', context=context)
