from .models import Patient
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Payment, Doctor, Admin,Employee

@receiver(pre_save, sender=Payment)
def generate_payment_id(sender, instance, **kwargs):
    if not instance.payment_id:
        # if no payment_id is provided, generate a new one
        last_payment = Payment.objects.order_by('-payment_id').first()
        if last_payment:
            last_payment_id = int(last_payment.payment_id)
            instance.payment_id = str(last_payment_id + 1)
        else:
            instance.payment_id = '1'


@receiver(pre_save, sender=Patient)
def generate_patient_id(sender, instance, **kwargs):
    if not instance.patient_id:
        last_patient = Patient.objects.order_by('-patient_id').first()
        if last_patient:
            last_patient_id = int(last_patient.patient_id)
            instance.patient_id = str(last_patient_id + 1)
        else:
            instance.patient_id = '1001'


@receiver(pre_save, sender=Employee)
def generate_employee_id(sender, instance, **kwargs):
    if not instance.employee_id:
        last_employee = Employee.objects.order_by('-employee_id').first()
        if last_employee:
            last_employee_id = int(last_employee.employee_id)
            instance.employee_id = str(last_employee_id + 1)
        else:
            instance.employee_id = '5001'


@receiver(pre_save, sender=Doctor)
def generate_doctor_id(sender, instance, **kwargs):
    if not instance.employee_id:
        last_doctor = Doctor.objects.order_by('-employee_id').first()
        if last_doctor:
            last_doctor_id = int(last_doctor.employee_id)
            instance.employee_id = str(last_doctor_id + 1)
        else:
            instance.employee_id = '3001'
            

def search_by_name_or_id(model, query):
    try:
        if model == Patient:
            obj = model.objects.filter(patient_id=int(query))
        
        elif model == Doctor or model ==Employee:
            obj = model.objects.filter(employee_id=int(query))

        
        
    except:
        try:    
            obj = model.objects.filter(name=query)    
            print(obj)
        except model.DoesNotExist:
            obj = None
    return obj