
from django.db import models
from django.contrib.auth.models import User


# =========================================================
# USER PROFILE
# =========================================================

class Profile(models.Model):

    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =========================================================
# JOB
# =========================================================

class Job(models.Model):

    employer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        null=True,
        blank=True
    )

    title = models.CharField(
        max_length=100
    )

    company = models.CharField(
        max_length=100
    )

    location = models.CharField(
        max_length=100
    )

    salary = models.CharField(
        max_length=50
    )

    description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.title


# =========================================================
# APPLICATION
# =========================================================

class Application(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shortlisted', 'Shortlisted'),
        ('Rejected', 'Rejected'),
        ('Selected', 'Selected'),
    )

    # -----------------------------------------------------
    # JOB APPLIED FOR
    # -----------------------------------------------------

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # JOB SEEKER WHO APPLIED
    # -----------------------------------------------------

    applicant = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='job_applications',
        null=True,
        blank=True
    )

    # -----------------------------------------------------
    # APPLICANT DETAILS
    # -----------------------------------------------------

    fullname = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    phone = models.CharField(
        max_length=15
    )

    qualification = models.CharField(
        max_length=100
    )

    resume = models.FileField(
        upload_to='resumes/',
        blank=True,
        null=True
    )

    # -----------------------------------------------------
    # APPLICATION STATUS
    # -----------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    # -----------------------------------------------------
    # APPLICATION DATE
    # -----------------------------------------------------

    applied_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        if self.job:
            return f"{self.fullname} - {self.job.title}"

        return self.fullname