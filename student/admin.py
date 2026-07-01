from django.contrib import admin
from .models import Department, Doctors, Booking, CustomUser, MedicalReport


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("dep_name",)
    search_fields = ("dep_name",)


@admin.register(Doctors)
class DoctorsAdmin(admin.ModelAdmin):
    list_display = (
        "doc_name",
        "doc_spec",
        "dep_name",
        "experience",
        "available",
    )

    list_filter = (
        "dep_name",
        "available",
    )

    search_fields = (
        "doc_name",
        "doc_spec",
    )


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):

    list_display = (
        "patient_name",
        "doctor",
        "appointment_date",
        "appointment_time",
        "status",
        "created_at",
    )

    list_filter = (
        "status",
        "doctor",
        "appointment_date",
    )

    search_fields = (
        "patient_name",
        "patient_email",
        "doctor__doc_name",
    )

    ordering = (
        "-created_at",
    )


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "username",
        "email",
        "role",
    )


@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = (
        "report_name",
        "patient",
        "uploaded_at",
    )