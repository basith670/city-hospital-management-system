from django.db import models
from django.contrib.auth.models import AbstractUser


# =========================
# Department Model
# =========================

class Department(models.Model):
    dep_name = models.CharField(max_length=100)
    dep_description = models.TextField()

    dep_image = models.ImageField(
        upload_to="departments/"
    )

    def __str__(self):
        return self.dep_name


# =========================
# Doctors Model
# =========================

class Doctors(models.Model):
    doc_name = models.CharField(max_length=100)
    doc_spec = models.CharField(max_length=100)

    dep_name = models.ForeignKey(
        Department,
        on_delete=models.CASCADE
    )

    doc_image = models.ImageField(
        upload_to="doctors/"
    )

    experience = models.PositiveIntegerField(default=1)

    qualification = models.CharField(
        max_length=150
    )

    available = models.BooleanField(
        default=True
    )

    def __str__(self):
        return self.doc_name


# =========================
# Booking Model
# =========================

class Booking(models.Model):

    STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    )

    patient_name = models.CharField(max_length=100)

    patient_email = models.EmailField()

    patient_phone = models.CharField(max_length=20)

    doctor = models.ForeignKey(
        Doctors,
        on_delete=models.CASCADE
    )

    appointment_date = models.DateField()

    appointment_time = models.TimeField()

    reason = models.TextField(
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.doc_name}"


# =========================
# Custom User Model
# =========================

class CustomUser(AbstractUser):

    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return self.username


# =========================
# Medical Report Model
# =========================

class MedicalReport(models.Model):

    patient = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    report_name = models.CharField(max_length=100)

    report_file = models.FileField(
        upload_to="reports/"
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.report_name