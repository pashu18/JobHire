from django.shortcuts import render, get_object_or_404, redirect
from django.db import models  # ✅ Required for Q lookups
from django.db.models import Count
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from .models import Job, Application
from .forms import ApplicationForm, JobForm


def job_list(request):
    query = request.GET.get('q')
    jobs = Job.objects.all().order_by('-posted_on')

    if query:
        jobs = jobs.filter(
            models.Q(title__icontains=query) |
            models.Q(company__icontains=query) |
            models.Q(location__icontains=query)
        )

    return render(request, 'hire/job_list.html', {'jobs': jobs, 'query': query})


def job_detail(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    return render(request, 'hire/job_detail.html', {'job': job})


def apply_job(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm()
    return render(request, 'hire/apply_job.html', {'form': form, 'job': job})


from django.views.decorators.http import require_POST

@staff_member_required
def view_applications(request, job_id):
    job = get_object_or_404(Job, pk=job_id)
    applications = job.application_set.all().order_by('-applied_on')

    if request.method == 'POST':
        app_id = request.POST.get('app_id')
        new_status = request.POST.get('status')
        application = get_object_or_404(Application, id=app_id, job=job)
        application.status = new_status
        application.save()
        messages.success(request, f"✅ Status updated for {application.name}")

    return render(request, 'hire/view_applications.html', {
        'job': job,
        'applications': applications
    })



@staff_member_required
def hr_dashboard(request):
    jobs = Job.objects.annotate(app_count=Count('application')).order_by('-posted_on')
    return render(request, 'hire/hr_dashboard.html', {'jobs': jobs})


@staff_member_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Job posted successfully!")
            return redirect('hr_dashboard')
    else:
        form = JobForm()
    return render(request, 'hire/post_job.html', {'form': form})








