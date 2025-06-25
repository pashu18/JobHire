from django.urls import path
from . import views


urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),
    path('hr-dashboard/', views.hr_dashboard, name='hr_dashboard'),
    path('post-job/', views.post_job, name='post_job'), 
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
]
