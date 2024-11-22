from django.contrib import admin
from .models import JobListing

class JobListingAdmin(admin.ModelAdmin):
    list_display = ('job_title', 'company', 'location', 'salary')  # Customize as per your model fields

admin.site.register(JobListing, JobListingAdmin)