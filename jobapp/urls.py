from django.urls import path

from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Login
    path(
        "login/",
        views.login,
        name="login"
    ),

    path(
        "job-seeker-login/",
        views.job_seeker_login,
        name="job_seeker_login"
    ),

    path(
        "employer-login/",
        views.employer_login,
        name="employer_login"
    ),

    # Register
    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "job-seeker-register/",
        views.job_seeker_register,
        name="job_seeker_register"
    ),

    path(
        "employer-register/",
        views.employer_register,
        name="employer_register"
    ),

    # Jobs
    path(
        "jobs/",
        views.jobs,
        name="jobs"
    ),

    # Apply
    path(
        "apply/",
        views.apply,
        name="apply"
    ),

    # My applications
    path(
        "my-applications/",
        views.my_applications,
        name="my_applications"
    ),

    # Employer
    path(
        "employer-dashboard/",
        views.employer_dashboard,
        name="employer_dashboard"
    ),

    path(
        "employer/add-job/",
        views.employer_add_job,
        name="employer_add_job"
    ),

    path(
        "employer/delete-job/<int:job_id>/",
        views.delete_job,
        name="delete_job"
    ),

    path(
        "employer/applications/",
        views.employer_applications,
        name="employer_applications"
    ),

    path(
        "employer/application/<int:application_id>/status/",
        views.update_application_status,
        name="update_application_status"
    ),

    # Other pages
    path(
        "about/",
        views.about,
        name="about"
    ),

    path(
        "contact/",
        views.contact,
        name="contact"
    ),

    path(
        "profile/",
        views.profile,
        name="profile"
    ),

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    # Logout
    path(
        "logout/",
        views.logout_user,
        name="logout"
    ),

    # Password
    path(
        "change-password/",
        views.change_password,
        name="change_password"
    ),

    path(
        "forgot-password/",
        views.forgot_password,
        name="forgot_password"
    ),

]