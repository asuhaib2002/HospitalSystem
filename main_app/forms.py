from django import forms
from .models import Patient, Payment, Doctor, User

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'name',
            'mobile_no',
            'email',
            'gender',
            'dob',
            'address',
            'occupation',
            'guardianname',
            'guardianphonenumber',
            'guardianrelation',
            'insurance',
        ]


class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'name',
            'mobile_no',
            'gender',
            'dob',
            'address',
            'picture',
        ]



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
        ]



class PatientSearchForm(forms.Form):
    name = forms.CharField(max_length=100)

    

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = [
            'amount',
            'patient',
        ]
