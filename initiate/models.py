from django.db import models
from django.utils.translation import gettext_lazy as _

class Process(models.Model):
    class ProcessStatus(models.IntegerChoices):
        FILE_UPLOADING = 0, _("File uploading")
        RUNNING = 1, _("Running")
        COMPLETED = 2, _("Completed")
        FAILED = 3, _("Failed")
    job_title = models.CharField(max_length=120)
    required_skills = models.CharField(max_length=120)
    min_experience_years = models.IntegerField()
    must_have_keywords = models.CharField(max_length=120)
    preferred_education = models.CharField(max_length=120)
    status = models.IntegerField(choices=ProcessStatus, default=ProcessStatus.FILE_UPLOADING)

class ProcessFile(models.Model):
    class ProcessFileStatus(models.IntegerChoices):
        FILE_UPLOADED = 0, _("File uploaded")
        COMPLETED = 1, _("Completed")
        FAILED = 2, _("Failed")
    process = models.ForeignKey(Process, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='process_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=ProcessFileStatus, default=ProcessFileStatus.FILE_UPLOADED)
    candidate_name = models.CharField(max_length=120, null=True)
    candidate_experience_years = models.IntegerField(null=True)
    candidate_skills = models.CharField(max_length=120, null=True)
    candidate_projects = models.CharField(max_length=120, null=True)
    candidate_education = models.CharField(max_length=120, null=True)
    score = models.IntegerField(null=True)
    remarks = models.CharField(max_length=120, null=True)
