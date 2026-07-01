from django.urls import path
from . import views

urlpatterns = [

    # ------------------------
    # Authentication
    # ------------------------

    path('', views.user_login, name='login'),

    path('logout/', views.user_logout, name='logout'),

    path(
        'doctor-register/',
        views.doctor_register,
        name='doctor_register'
    ),

    path(
        'patient-register/',
        views.patient_register,
        name='patient_register'
    ),

    # ------------------------
    # Dashboards
    # ------------------------

    path(
        'doctor-dashboard/',
        views.doctor_dashboard,
        name='doctor_dashboard'
    ),

    path(
        'patient-dashboard/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

    # ------------------------
    # Medical Reports
    # ------------------------

    path(
        'upload-report/',
        views.upload_report,
        name='upload_report'
    ),

    path(
        'view-reports/',
        views.view_reports,
        name='view_reports'
    ),

    # ------------------------
    # Hospital Website
    # ------------------------

    path('home/', views.home, name='home'),

    path('about/', views.about, name='about'),

    path('booking/', views.booking, name='booking'),

    path('doctors/', views.doctors, name='doctors'),

    path(
        'departments/',
        views.departments,
        name='departments'
    ),

    path('contact/', views.contact, name='contact'),

    path(
    "confirmation/<int:booking_id>/",
    views.confirmation,
    name="confirmation"
),

path(
    "appointments/",
    views.manage_appointments,
    name="manage_appointments"
),

path(
    "appointment/<int:booking_id>/<str:status>/",
    views.update_appointment_status,
    name="update_appointment_status",
),

]