from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings

from .models import (
    Department,
    Doctors,
    Booking,
    MedicalReport
)

from .forms import (
    BookingForm,
    DoctorRegisterForm,
    PatientRegisterForm,
    MedicalReportForm
)
import logging

logger = logging.getLogger(__name__)


# ==========================================
# AUTHENTICATION
# ==========================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if user.role == "doctor":
                return redirect("doctor_dashboard")

            return redirect("patient_dashboard")

        return render(
            request,
            "login.html",
            {
                "error": "Invalid Username or Password"
            }
        )

    return render(request, "login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


def doctor_register(request):

    form = DoctorRegisterForm()

    if request.method == "POST":

        form = DoctorRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = "doctor"
            user.save()

            return redirect("login")

    return render(
        request,
        "doctor_register.html",
        {
            "form": form
        }
    )


def patient_register(request):

    form = PatientRegisterForm()

    if request.method == "POST":

        form = PatientRegisterForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.role = "patient"
            user.save()

            return redirect("login")

    return render(
        request,
        "patient_register.html",
        {
            "form": form
        }
    )


# ==========================================
# PUBLIC WEBSITE
# ==========================================

def home(request):
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")


def doctors(request):

    doctors = Doctors.objects.select_related("dep_name").all()

    return render(
        request,
        "doctors.html",
        {
            "doctors": doctors
        }
    )


def departments(request):

    dept = Department.objects.all()

    return render(
        request,
        "departments.html",
        {
            "dept": dept
        }
    )


def contact(request):
    return render(request, "contact.html")


# ==========================================
# BOOK APPOINTMENT
# ==========================================

@login_required(login_url="login")

def booking(request):

    doctor_id = request.GET.get("doctor")

    if request.method == "POST":

        form = BookingForm(request.POST)

        if form.is_valid():

            appointment = form.save()

            # ==============================

            # EMAIL CONFIG DEBUG

            # ==============================

            print("=" * 60)

            print("EMAIL CONFIG")

            print("HOST:", settings.EMAIL_HOST)

            print("PORT:", settings.EMAIL_PORT)

            print("USER:", settings.EMAIL_HOST_USER)

            print("PASSWORD EXISTS:", bool(settings.EMAIL_HOST_PASSWORD))

            print("=" * 60)

            # ==============================

            # EMAIL TO ADMIN

            # ==============================

            try:

                send_mail(

                    subject="New Appointment",

                    message=f"""

Patient : {appointment.patient_name}

Doctor : {appointment.doctor}

Date : {appointment.appointment_date}

Time : {appointment.appointment_time}

Reason :

{appointment.reason}

""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[settings.EMAIL_HOST_USER],

                    fail_silently=False,

                )

                print("✅ Admin email sent successfully.")

            except Exception:

                logger.exception("Failed to send admin email")

            # ==============================

            # EMAIL TO PATIENT

            # ==============================

            try:

                send_mail(

                    subject="Appointment Confirmed",

                    message=f"""

Dear {appointment.patient_name},

Your appointment has been booked successfully.

Doctor:

{appointment.doctor}

Date:

{appointment.appointment_date}

Time:

{appointment.appointment_time}

Thank you for choosing City Hospital.

Regards,

City Hospital

""",

                    from_email=settings.DEFAULT_FROM_EMAIL,

                    recipient_list=[appointment.patient_email],

                    fail_silently=False,

                )

                print("✅ Patient email sent successfully.")

            except Exception:

                logger.exception("Failed to send patient email")

            return redirect(

                "confirmation",

                booking_id=appointment.id

            )

    else:

        form = BookingForm()

        if doctor_id:

            form.fields["doctor"].initial = doctor_id

    return render(

        request,

        "booking.html",

        {

            "form": form

        }

    )


# ==========================================
# CONFIRMATION
# ==========================================

@login_required(login_url="login")
def confirmation(request, booking_id):

    booking = Booking.objects.get(id=booking_id)

    return render(
        request,
        "confirmation.html",
        {
            "booking": booking
        }
    )


# ==========================================
# DOCTOR DASHBOARD
# ==========================================

@login_required(login_url="login")
def doctor_dashboard(request):

    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    appointments = Booking.objects.all().order_by(
        "-appointment_date",
        "-appointment_time"
    )

    reports = MedicalReport.objects.all().order_by("-uploaded_at")[:5]

    context = {

        "appointments": appointments,

        "reports": reports,

        "appointment_count": appointments.count(),

        "patient_count": Booking.objects.values(
            "patient_email"
        ).distinct().count(),

        "doctor_count": Doctors.objects.count(),

        "department_count": Department.objects.count(),

        "report_count": MedicalReport.objects.count(),

        "active_page": "dashboard",

    }

    return render(
        request,
        "doctor_dashboard.html",
        context
    )

from django.db.models import Q

@login_required(login_url="login")
def manage_appointments(request):

    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    appointments = Booking.objects.all().order_by(
        "appointment_date",
        "appointment_time"
    )

    search = request.GET.get("search")
    status = request.GET.get("status")

    if search:

        appointments = appointments.filter(

            Q(patient_name__icontains=search) |

            Q(patient_email__icontains=search) |

            Q(patient_phone__icontains=search)

        )

    if status and status != "All":

        appointments = appointments.filter(
            status=status
        )

    return render(
        request,
        "manage_appointments.html",
        {
            "appointments": appointments,
            "search": search,
            "status": status,
            "active_page": "appointments",
        }
    )

@login_required(login_url="login")
def update_appointment_status(request, booking_id, status):

    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    appointment = Booking.objects.get(id=booking_id)

    if status in ["Pending", "Confirmed", "Completed", "Cancelled"]:
        appointment.status = status
        appointment.save()

    return redirect("manage_appointments")

# ==========================================
# PATIENT DASHBOARD
# ==========================================

@login_required(login_url="login")
def patient_dashboard(request):

    if request.user.role != "patient":
        return redirect("doctor_dashboard")

    appointments = Booking.objects.filter(
        patient_email=request.user.email
    ).order_by("-appointment_date")

    reports = MedicalReport.objects.filter(
        patient=request.user
    )

    context = {
    "appointments": appointments,
    "reports": reports,
    "appointment_count": appointments.count(),
    "report_count": reports.count(),
    "active_page": "dashboard",
}

    return render(
        request,
        "patient_dashboard.html",
        context
    )


# ==========================================
# UPLOAD REPORT
# ==========================================

@login_required(login_url="login")
def upload_report(request):

    if request.user.role != "patient":
        return redirect("doctor_dashboard")

    form = MedicalReportForm()

    if request.method == "POST":

        form = MedicalReportForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            report = form.save(commit=False)
            report.patient = request.user
            report.save()



            print("=" * 50)

            print("FILE NAME:", report.report_file.name)

            print("FILE PATH:", report.report_file.path)

            print("FILE EXISTS:", os.path.exists(report.report_file.path))

            print("=" * 50)

            return redirect("patient_dashboard")

    return render(
    request,
    "upload_report.html",
    {
        "form": form,
        "active_page": "upload_report"
    }
)



# ==========================================
# VIEW REPORTS
# ==========================================

@login_required(login_url="login")
def view_reports(request):

    if request.user.role != "doctor":
        return redirect("patient_dashboard")

    reports = MedicalReport.objects.all()

    return render(
    request,
    "view_reports.html",
    {
        "reports": reports,
        "active_page": "view_reports"
    }
)