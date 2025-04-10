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
