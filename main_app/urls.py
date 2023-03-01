from django.contrib import admin
from django.urls import path
from .views import Home, CustomLoginView, dashboard, AddDoctor, AddEmployee,doctor_list,doctorview,employee_list,employeeview,patient_list,patientview
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', Home, name='home'),
    path('login/',CustomLoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/',dashboard, name='dashboard'),
    path('add-doctor/',AddDoctor, name='add-doctor'),
    path('add-employee/',AddEmployee, name='add-employee'),
    path('doctor_list/',doctor_list,name='doctor_list'),
    path('doctorview/<str:id>/', doctorview ,name="doctorview"),
    path('employee_list/',employee_list,name='employee_list'),
    path('employeeview/<str:id>/', employeeview ,name="employeeview"),
    path('patient_list/',patient_list,name='patient_list'),
    path('patientview/<str:id>/', patientview ,name="patientview"),

    

    

]

