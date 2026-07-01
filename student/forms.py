from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Booking, CustomUser, MedicalReport


class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "patient_name",
            "patient_email",
            "patient_phone",
            "doctor",
            "appointment_date",
            "appointment_time",
            "reason",
        ]

        widgets = {

            "patient_name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Full Name",
                }
            ),

            "patient_email": forms.EmailInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Email Address",
                }
            ),

            "patient_phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Enter Phone Number",
                }
            ),

            "doctor": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),

            "appointment_date": forms.DateInput(
                attrs={
                    "class": "form-control",
                    "type": "date",
                }
            ),

            "appointment_time": forms.TimeInput(
                attrs={
                    "class": "form-control",
                    "type": "time",
                }
            ),

            "reason": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Briefly describe your symptoms or reason for the appointment",
                }
            ),
        }


class DoctorRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class PatientRegisterForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        ]


class MedicalReportForm(forms.ModelForm):

    class Meta:
        model = MedicalReport
        fields = [
            'report_name',
            'report_file'
        ]