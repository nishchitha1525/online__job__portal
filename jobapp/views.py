from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages

from .models import Job, Application, Profile


# =========================================================
# HOME
# =========================================================

def home(request):
    return render(request, "home.html")


# =========================================================
# LOGIN SELECTION
# =========================================================

def login(request):
    return render(request, "login.html")


# =========================================================
# JOB SEEKER LOGIN
# =========================================================

def job_seeker_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                profile = Profile.objects.get(user=user)

                if profile.role == "job_seeker":

                    # Login user
                    auth_login(request, user)

                    # Show login success page
                    return render(
                        request,
                        "login_success.html"
                    )

                else:

                    messages.error(
                        request,
                        "This is an Employer account. Please use Employer Login."
                    )

            except Profile.DoesNotExist:

                messages.error(
                    request,
                    "Profile not found. Please register again."
                )

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

    # IMPORTANT:
    # Show login page when opening the URL normally
    return render(
        request,
        "job_seeker_login.html"
    )


# =========================================================
# EMPLOYER LOGIN
# =========================================================

def employer_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:
                profile = Profile.objects.get(user=user)

                if profile.role == "employer":

                    auth_login(request, user)

                    # Clear old messages
                    storage = messages.get_messages(request)
                    list(storage)

                    return render(
                        request,
                        "employer_login_success.html"
                    )

                else:

                    messages.error(
                        request,
                        "This is a Job Seeker account. Please use Job Seeker Login."
                    )

            except Profile.DoesNotExist:

                messages.error(
                    request,
                    "Profile not found. Please register again."
                )

        else:

            messages.error(
                request,
                "Invalid Username or Password."
            )

    return render(
        request,
        "employer_login.html"
    )


# =========================================================
# REGISTER SELECTION
# =========================================================

def register(request):
    return render(request, "register.html")


# =========================================================
# JOB SEEKER REGISTER
# =========================================================

def job_seeker_register(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check empty fields
        if not fullname or not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill all fields."
            )

            return render(
                request,
                "job_seeker_register.html"
            )

        # Password check
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match!"
            )

            return render(
                request,
                "job_seeker_register.html"
            )

        # Username check
        if User.objects.filter(username=fullname).exists():

            messages.error(
                request,
                "Username already exists!"
            )

            return render(
                request,
                "job_seeker_register.html"
            )

        # Email check
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists!"
            )

            return render(
                request,
                "job_seeker_register.html"
            )

        # Create user
        user = User.objects.create_user(
            username=fullname,
            email=email,
            password=password
        )

        # Create profile
        Profile.objects.create(
            user=user,
            role="job_seeker"
        )

        messages.success(
            request,
            "Job Seeker Registration Successful! Please Login."
        )

        return redirect("job_seeker_login")

    return render(
        request,
        "job_seeker_register.html"
    )


# =========================================================
# EMPLOYER REGISTER
# =========================================================

def employer_register(request):

    if request.method == "POST":

        fullname = request.POST.get("fullname", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check empty fields
        if not fullname or not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill all fields."
            )

            return render(
                request,
                "employer_register.html"
            )

        # Password check
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match!"
            )

            return render(
                request,
                "employer_register.html"
            )

        # Username check
        if User.objects.filter(username=fullname).exists():

            messages.error(
                request,
                "Username already exists!"
            )

            return render(
                request,
                "employer_register.html"
            )

        # Email check
        if User.objects.filter(email=email).exists():

            messages.error(
                request,
                "Email already exists!"
            )

            return render(
                request,
                "employer_register.html"
            )

        # Create employer
        user = User.objects.create_user(
            username=fullname,
            email=email,
            password=password
        )

        # Create employer profile
        Profile.objects.create(
            user=user,
            role="employer"
        )

        messages.success(
            request,
            "Employer Registration Successful! Please Login."
        )

        return redirect("employer_login")

    return render(
        request,
        "employer_register.html"
    )


# =========================================================
# JOB SEEKER - VIEW JOBS
# =========================================================

def jobs(request):

    title = request.GET.get("title", "").strip()
    location = request.GET.get("location", "").strip()

    jobs_list = Job.objects.all().order_by("-id")

    if title:

        jobs_list = jobs_list.filter(
            title__icontains=title
        )

    if location:

        jobs_list = jobs_list.filter(
            location__icontains=location
        )

    return render(
        request,
        "jobs.html",
        {
            "jobs": jobs_list
        }
    )


# =========================================================
# APPLY FOR JOB
# =========================================================

def apply(request):

    # User must login
    if not request.user.is_authenticated:

        messages.error(
            request,
            "Please login as a Job Seeker to apply for a job."
        )

        return redirect("job_seeker_login")

    # Check Job Seeker profile
    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Profile not found."
        )

        return redirect("job_seeker_login")

    if profile.role != "job_seeker":

        messages.error(
            request,
            "Only Job Seekers can apply for jobs."
        )

        return redirect("jobs")

    # Get Job ID
    job_id = request.GET.get("job_id")

    if not job_id:
        job_id = request.POST.get("job_id")

    # Job ID missing
    if not job_id:

        messages.error(
            request,
            "Please select a job first."
        )

        return redirect("jobs")

    # Get selected job
    job = get_object_or_404(
        Job,
        id=job_id
    )

    # =====================================================
    # POST - SUBMIT APPLICATION
    # =====================================================

    if request.method == "POST":

        fullname = request.POST.get(
            "fullname",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        qualification = request.POST.get(
            "qualification",
            ""
        ).strip()

        resume = request.FILES.get("resume")

        # Check details
        if (
            not fullname
            or not email
            or not phone
            or not qualification
            or not resume
        ):

            messages.error(
                request,
                "Please fill all details and upload your resume."
            )

            return render(
                request,
                "apply.html",
                {
                    "job": job
                }
            )

        # =================================================
        # CHECK DUPLICATE APPLICATION
        # =================================================

        already_applied = Application.objects.filter(
            applicant=request.user,
            job=job
        ).exists()

        if already_applied:

            messages.error(
                request,
                "You have already applied for this job."
            )

            return render(
                request,
                "apply.html",
                {
                    "job": job
                }
            )

        # =================================================
        # CREATE APPLICATION
        # =================================================

        Application.objects.create(
            applicant=request.user,
            job=job,
            fullname=fullname,
            email=email,
            phone=phone,
            qualification=qualification,
            resume=resume
        )

        messages.success(
            request,
            "Application submitted successfully!"
        )

        return redirect("my_applications")

    # =====================================================
    # GET - SHOW APPLICATION FORM
    # =====================================================

    return render(
        request,
        "apply.html",
        {
            "job": job
        }
    )


# =========================================================
# EMPLOYER DASHBOARD
# =========================================================

def employer_dashboard(request):

    if not request.user.is_authenticated:

        return redirect("employer_login")

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Employer profile not found."
        )

        return redirect("employer_login")

    if profile.role != "employer":

        messages.error(
            request,
            "Only employers can access this page."
        )

        return redirect("jobs")

    # Only this employer's jobs
    posted_jobs = Job.objects.filter(
        employer=request.user
    ).order_by("-id")

    return render(
        request,
        "employer_dashboard.html",
        {
            "posted_jobs": posted_jobs
        }
    )


# =========================================================
# EMPLOYER ADD JOB
# =========================================================

def employer_add_job(request):

    if not request.user.is_authenticated:

        return redirect("employer_login")

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Profile not found."
        )

        return redirect("employer_login")

    if profile.role != "employer":

        messages.error(
            request,
            "Only employers can add jobs."
        )

        return redirect("jobs")

    if request.method == "POST":

        title = request.POST.get(
            "title",
            ""
        ).strip()

        company = request.POST.get(
            "company",
            ""
        ).strip()

        location = request.POST.get(
            "location",
            ""
        ).strip()

        salary = request.POST.get(
            "salary",
            ""
        ).strip()

        description = request.POST.get(
            "description",
            ""
        ).strip()

        # Required fields
        if not title or not company or not location:

            messages.error(
                request,
                "Please fill all required fields."
            )

            return render(
                request,
                "employer_add_job.html"
            )

        # Create job
        Job.objects.create(
            employer=request.user,
            title=title,
            company=company,
            location=location,
            salary=salary,
            description=description
        )

        messages.success(
            request,
            "Job Posted Successfully!"
        )

        return redirect("employer_dashboard")

    return render(
        request,
        "employer_add_job.html"
    )


# =========================================================
# EMPLOYER DELETE JOB
# =========================================================

def delete_job(request, job_id):

    if not request.user.is_authenticated:

        return redirect("employer_login")

    # Only delete own job
    job = get_object_or_404(
        Job,
        id=job_id,
        employer=request.user
    )

    if request.method == "POST":

        job.delete()

        messages.success(
            request,
            "Job Deleted Successfully!"
        )

        return redirect("employer_dashboard")

    return render(
        request,
        "delete_job.html",
        {
            "job": job
        }
    )


# =========================================================
# EMPLOYER VIEW APPLICATIONS
# =========================================================

def employer_applications(request):

    if not request.user.is_authenticated:

        return redirect("employer_login")

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Employer profile not found."
        )

        return redirect("employer_login")

    if profile.role != "employer":

        messages.error(
            request,
            "Only employers can view applications."
        )

        return redirect("jobs")

    # Applications for this employer's jobs only
    applications = Application.objects.filter(
        job__employer=request.user
    ).select_related(
        "job",
        "applicant"
    ).order_by("-id")

    return render(
        request,
        "employer_applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# EMPLOYER - UPDATE APPLICATION STATUS
# =========================================================

def update_application_status(
    request,
    application_id
):

    if not request.user.is_authenticated:

        return redirect("employer_login")

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Employer profile not found."
        )

        return redirect("employer_login")

    if profile.role != "employer":

        messages.error(
            request,
            "Only employers can update application status."
        )

        return redirect("jobs")

    # Only applications for this employer's jobs
    application = get_object_or_404(
        Application,
        id=application_id,
        job__employer=request.user
    )

    if request.method == "POST":

        status = request.POST.get("status")

        allowed_status = [
            "Pending",
            "Accepted",
            "Rejected"
        ]

        if status in allowed_status:

            application.status = status
            application.save()

            

        else:

            messages.error(
                request,
                "Invalid application status."
            )

    return redirect(
        "employer_applications"
    )


# =========================================================
# ABOUT
# =========================================================

def about(request):

    return render(
        request,
        "about.html"
    )


# =========================================================
# CONTACT
# =========================================================

def contact(request):

    return render(
        request,
        "contact.html"
    )


# =========================================================
# PROFILE
# =========================================================

def profile(request):

    if not request.user.is_authenticated:

        return redirect("login")

    return render(
        request,
        "profile.html"
    )


# =========================================================
# JOB SEEKER DASHBOARD
# =========================================================

def dashboard(request):

    if not request.user.is_authenticated:

        return redirect("job_seeker_login")

    try:

        profile = Profile.objects.get(
            user=request.user
        )

    except Profile.DoesNotExist:

        messages.error(
            request,
            "Profile not found."
        )

        return redirect("login")

    if profile.role != "job_seeker":

        return redirect("employer_dashboard")

    jobs_list = Job.objects.all().order_by("-id")

    return render(
        request,
        "seeker_dashboard.html",
        {
            "jobs": jobs_list
        }
    )


# =========================================================
# LOGOUT
# =========================================================

# =========================================================
# LOGOUT
# =========================================================

def logout_user(request):

    logout(request)

    return redirect("home")


# =========================================================
# MY APPLICATIONS
# =========================================================

def my_applications(request):

    if not request.user.is_authenticated:

        return redirect("job_seeker_login")

    # Only current user's applications
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related(
        "job"
    ).order_by("-id")

    return render(
        request,
        "my_applications.html",
        {
            "applications": applications
        }
    )


# =========================================================
# CHANGE PASSWORD
# =========================================================

def change_password(request):

    if not request.user.is_authenticated:

        return redirect("login")

    if request.method == "POST":

        old_password = request.POST.get(
            "old_password"
        )

        new_password = request.POST.get(
            "new_password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        # Check old password
        if not request.user.check_password(old_password):

            messages.error(
                request,
                "Current password is incorrect."
            )

            return render(
                request,
                "change_password.html"
            )

        # Check empty password
        if not new_password or not confirm_password:

            messages.error(
                request,
                "Please enter the new password."
            )

            return render(
                request,
                "change_password.html"
            )

        # Check new passwords
        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return render(
                request,
                "change_password.html"
            )

        # Change password
        request.user.set_password(
            new_password
        )

        request.user.save()

        logout(request)

        messages.success(
            request,
            "Password Changed Successfully! Please Login Again."
        )

        return redirect("login")

    return render(
        request,
        "change_password.html"
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get(
            "email",
            ""
        ).strip()

        password = request.POST.get(
            "password"
        )

        confirm_password = request.POST.get(
            "confirm_password"
        )

        # Check empty fields
        if not email or not password or not confirm_password:

            messages.error(
                request,
                "Please fill all fields."
            )

            return render(
                request,
                "forgot_password.html"
            )

        # Check passwords
        if password != confirm_password:

            messages.error(
                request,
                "Passwords do not match!"
            )

            return render(
                request,
                "forgot_password.html"
            )

        # Find user
        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            messages.error(
                request,
                "Email not found!"
            )

            return render(
                request,
                "forgot_password.html"
            )

        # Change password
        user.set_password(password)
        user.save()

        messages.success(
            request,
            "Password Reset Successfully! Please Login."
        )

        return redirect("login")

    return render(
        request,
        "forgot_password.html"
    )
