from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your models here.


class Admin(models.Model):
    GenderChoice=(
        ('male','MALE'),
        ('female','FEMALE'),
        ('unspecified','UNSPECIFIED'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    employee_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    is_admin = models.BooleanField(default=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    name = models.CharField(max_length = 50)
    mobile_no = models.CharField(max_length = 15)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length = 20, choices= GenderChoice) 
    dob = models.DateField()
    regdate = models.DateField(auto_now=False, auto_now_add=True)
    address = models.CharField(max_length = 100)
    picture = models.ImageField(null=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate an employee ID if one doesn't already exist
        if not self.employee_id:
            # Get the highest existing employee ID
            highest_employee_id = Admin.objects.aggregate(models.Max('employee_id'))['employee_id__max']

            # Generate a new employee ID that is one higher than the highest existing ID
            new_employee_id = int(highest_employee_id) + 1 if highest_employee_id else 1000

            # Format the new employee ID as a string with leading zeros
            self.employee_id = '{:04d}'.format(new_employee_id)

        # Call the parent save() method to save the model to the database
        super().save(*args, **kwargs)



class Employee(models.Model):
    GenderChoice=(
        ('male','MALE'),
        ('female','FEMALE'),
        ('unspecified','UNSPECIFIED'),
    )
     
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_employee = models.BooleanField(default=True)
    employee_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    name = models.CharField(max_length = 50)
    mobile_no = models.CharField(max_length = 15)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length = 20, choices= GenderChoice) 
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    picture = models.ImageField(null=True, blank=True)
    regdate = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
         return self.name




class Doctor(models.Model):
    GenderChoice=(
        ('male','MALE'),
        ('female','FEMALE'),
        ('unspecified','UNSPECIFIED'),
    )
     
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    is_admin = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=True)
    is_patient = models.BooleanField(default=False)
    employee_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    name = models.CharField(max_length = 50)
    mobile_no = models.CharField(max_length = 15)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length = 20, choices= GenderChoice) 
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    picture = models.ImageField(null=True, blank=True)
    regdate = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
         return self.name


    @classmethod
    def get_total(cls):
        return cls.objects.all().count()



class Patient(models.Model):
    GenderChoice=(
        ('male','MALE'),
        ('female','FEMALE'),
        ('unspecified','UNSPECIFIED'),
    )
     

    RelationChoice=(
        ('Brother','Brother'),
        ('Parent','Parent'),
        ('Spouse','Spouse'),
        ('Sister','Sister'),
        ('Son','Son'),
        ('Daughter','Daughter'),
        ('Other','Other'),
    ) 
    patient_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    name = models.CharField(max_length = 50)
    mobile_no = models.CharField(max_length = 15)
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length = 20, choices= GenderChoice) 
    dob = models.DateField()
    address = models.CharField(max_length = 100)
    picture = models.ImageField(null=True, blank=True)
    occupation = models.CharField(max_length=100)
    regdate = models.DateField(auto_now=False, auto_now_add=True)
    guardianname = models.CharField(max_length=100)
    guardianphonenumber = models.CharField(max_length = 15)
    guardianrelation = models.CharField(max_length=100, null = False,choices=RelationChoice)
    insurance = models.CharField(max_length=100)

    def __str__(self):
         return self.patient_id
    
        


    @classmethod
    def get_total(cls):
        return cls.objects.all().count()
        



class Payment(models.Model):
    payment_id = models.IntegerField(unique=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)

    def __str__(self):
         return str(self.amount)

    @classmethod
    def get_payments(cls, date):
        payments = cls.objects.filter(date=date)
        total_amount = payments.aggregate(Sum('amount'))['amount__sum']
        if total_amount is None:
            total_amount = 0
        
        return total_amount
    
    @classmethod
    def get_total_payments(cls):
        total_payments = cls.objects.aggregate(total=models.Sum('amount'))['total']
        return total_payments if total_payments is not None else 0