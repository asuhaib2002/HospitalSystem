from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .forms import *
from .models import Patient, Doctor, Employee
from django.http import HttpResponse,HttpResponseRedirect
from .tasks import *
from datetime import date





# Create your views here.

def Home(request):
    if request.user.is_authenticated:
        patient_creation_form = PatientForm()
        patient_search_form = PatientSearchForm()
        payment_form = PaymentForm()
        search_patient = Patient.objects.all()
        patient_names = Patient.objects.values_list('name', flat=True)
        search_list = list(search_patient) + list(patient_names)

        if request.method == 'POST':
            if 'patient_creation' in request.POST:
                patient_creation_form = PatientForm(request.POST)
                if patient_creation_form.is_valid():
                    print(request.POST.get('name',None))
                    # Process the form data and save the new patient
                    # Redirect to a success page, or back to the original page with a success message
                    patient_creation_form.save()
                    return redirect('home')

            elif 'patient_search' in request.POST:
                search_term  = request.POST.get('my-input-field')
                patients = search_by_name_or_id(Patient,search_term)

                context = {
                    'patient_creation_form': patient_creation_form,
                    'patient_search_form': patient_search_form,
                    'payment_form': payment_form,
                    'patients': patients,
                    'search_list':search_list,
                }
                return render(request, 'main_app/home.html', context)

            elif 'payment' in request.POST:
                payment_form = PaymentForm(request.POST)
                if payment_form.is_valid():
                    # Process the payment data and redirect to a success page
                    payment_form.save()
                    return redirect('home')

        context = {
            'patient_creation_form': patient_creation_form,
            'patient_search_form': patient_search_form,
            'payment_form': payment_form,
            'search_list':search_list,
        }
        return render(request, 'main_app/home.html', context)


    else :
        return render(request,'main_app/login.html')

    return render(request,'main_app/home.html')


def dashboard(request):
    if request.user.is_authenticated:
        total_income = Payment.get_total_payments()
        today_income = Payment.get_payments(date.today())
        total_patients = Patient.get_total()
        total_doctors = Doctor.get_total()

        context = {
            'total_income': total_income,
            'today_income': today_income,
            'total_patients': total_patients,
            'total_doctors' : total_doctors,
        }
        return render(request, 'main_app/dashboard.html', context)
    
    else:
        return redirect('login')



def AddDoctor(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('name')
            password = request.POST.get('password')
            re_password = request.POST.get('re-password')
            email = request.POST.get('email')
            address= request.POST.get('address')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            mobile_no = request.POST.get('mobile_no')
            image = request.POST.get('img')
            print(password,re_password)
            if password == re_password:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = None
                if user is None:
                    try:
                        validate_password(password)
                        user = User(username=username, email=email, password=password)
                        user.save()
                        print(user)
                        doctor = Doctor(user=user,name=name,mobile_no=mobile_no,email=email,gender=gender,dob=dob,address=address)
                        doctor.save()

                    except ValidationError as e:
                        # Password validation failed
                        return render(request, 'main_app/add-doctor.html', {'error': str(e)})

                else:
                    return render(request, 'main_app/add-doctor.html', {'error': 'Username already exists'})                
                    
            
            else:
                # Passwords don't match
                print('errer')
                return render(request, 'main_app/add-doctor.html', {'error': 'Passwords do not match'})                
        return render(request, 'main_app/add-doctor.html')



    

def doctorview(request, id):
    doctor = get_object_or_404(Doctor, employee_id=id)
    if request.method == 'POST':
        doctor.name = request.POST.get('name')
        doctor.email = request.POST.get('email')
        doctor.mobile_no = request.POST.get('mobile_no')
        doctor.address = request.POST.get('address')
        doctor.dob = request.POST.get('dob')
        doctor.gender = request.POST.get('gender')
        
        if request.POST.get('active',False) != doctor.user.is_active:
            doctor.user.is_active = request.POST.get('active',False)
            doctor.user.save()
        # doctor.picture = request.POST.get('picture')
        doctor.save()
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'main_app/doctor_view.html', {'doctor': doctor})
    
def doctor_list(request):
    search_doctor = Doctor.objects.all()
    doctor_id = Doctor.objects.values_list('employee_id', flat=True)
    search_list = list(search_doctor) + list(doctor_id)
    if request.method == 'POST':
        search_term  = request.POST.get('my-input-field', '')
        if search_term:
            doctors = search_by_name_or_id(Doctor,search_term)
            context = {'doctors': doctors, 'search_list':search_list}

        else:
            doctors = Doctor.objects.all()
            context = {'doctors': doctors, 'search_list':search_list}
        return render(request, 'main_app/doctor_list.html', context)


    doctors = Doctor.objects.all()
    context = {'doctors': doctors,'search_list':search_list}
    return render(request, 'main_app/doctor_list.html', context)



def employeeview(request, id):
    employee = get_object_or_404(Employee, employee_id=id)
    if request.method == 'POST':
        employee.name = request.POST.get('name')
        employee.email = request.POST.get('email')
        employee.mobile_no = request.POST.get('mobile_no')
        employee.address = request.POST.get('address')
        employee.dob = request.POST.get('dob')
        employee.gender = request.POST.get('gender')
        # doctor.picture = request.POST.get('picture')
        if request.POST.get('active',False) != employee.user.is_active:
            employee.user.is_active = request.POST.get('active',False)
            employee.user.save()
        employee.save()
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'main_app/employee_view.html', {'employee': employee})
    

def employee_list(request):
    search_employee = Employee.objects.all()
    Employee_id = Employee.objects.values_list('employee_id', flat=True)
    search_list = list(search_employee) + list(Employee_id)
    if request.method == 'POST':
        search_term  = request.POST.get('my-input-field', '')
        if search_term:
            employees = search_by_name_or_id(Employee,search_term)
            context = {'employees': employees, 'search_list': search_list}

        else:
            employees = Employee.objects.all()
            context = {'employees': employees, 'search_list': search_list}
        return render(request, 'main_app/employee_list.html', context)

    employees = Employee.objects.all()
    context = {'employees': employees,'search_list': search_list}
    return render(request, 'main_app/employee_list.html', context)

def patient_list(request):
    search_patient = Patient.objects.all()
    Patient_name = Patient.objects.values_list('name', flat=True)
    search_list = list(search_patient) + list(Patient_name)
    if request.method == 'POST':
        search_term  = request.POST.get('my-input-field', '')
        if search_term:
            patients = search_by_name_or_id(Patient,search_term)
            context = {'patients': patients, 'search_list': search_list}

        else:
            patients = Patient.objects.all()
            context = {'patients': patients, 'search_list': search_list}
        return render(request, 'main_app/patient_list.html', context)
    
    patients = Patient.objects.all()
    context = {'patients': patients, 'search_list': search_list}
    return render(request, 'main_app/patient_list.html', context)



def patientview(request, id):
    patient = get_object_or_404(Patient, patient_id=id)
    if request.method == 'POST':
        patient.name = request.POST.get('name')
        patient.email = request.POST.get('email')
        patient.mobile_no = request.POST.get('mobile_no')
        patient.address = request.POST.get('address')
        patient.dob = request.POST.get('dob')
        patient.gender = request.POST.get('gender')
        # doctor.picture = request.POST.get('picture')
        patient.save()
        return HttpResponseRedirect(request.path_info)
    else:
        return render(request, 'main_app/patient_view.html', {'patient': patient})



def AddEmployee(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            name = request.POST.get('name')
            password = request.POST.get('password')
            re_password = request.POST.get('re-password')
            email = request.POST.get('email')
            address= request.POST.get('address')
            dob = request.POST.get('dob')
            gender = request.POST.get('gender')
            mobile_no = request.POST.get('mobile_no')
            image = request.POST.get('img')
            print(password,re_password)
            if password == re_password:
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    user = None
                if user is None:
                    try:
                        validate_password(password)
                        user = User(username=username, email=email, password=password)
                        user.save()
                        print(user)
                        employee = Employee(user=user,name=name,mobile_no=mobile_no,email=email,gender=gender,dob=dob,address=address)
                        employee.save()

                    except ValidationError as e:
                        # Password validation failed
                        return render(request, 'main_app/add-employee.html', {'error': str(e)})

                else:
                    return render(request, 'main_app/add-employee.html', {'error': 'Username already exists'})                
                    
            
            else:
                # Passwords don't match
                print('errer')
                return render(request, 'main_app/add-employee.html', {'error': 'Passwords do not match'})                
        return render(request, 'main_app/add-employee.html')





class CustomLoginView(LoginView):
    template_name ='main_app\login.html'
    fields = ['__all__']
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('home')
