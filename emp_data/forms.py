from django import forms
from emp_data.models import Employee
from emp_data.models import Customer
from emp_data.models import Login
from emp_data.models import Customer_Requirements
from emp_data.models import addEmpToCustomer
from emp_data.models import TA_Resource
from emp_data.models import VmResource
from emp_data.models import Ta_resume
# This is for employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

#this is for customer
class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"

# this is for customer_requirement
class Customer_RequirementForm(forms.ModelForm):
    class Meta:
        model = Customer_Requirements
        fields = "__all__"

class addEmpToCustomerForm(forms.ModelForm):
    class Meta:
        model = addEmpToCustomer
        fields = "__all__"
        
class loginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = "__all__"

class UploadFileForm(forms.Form):
    file = forms.FileField()

#This is for TA Resource details.
class TA_Form(forms.ModelForm):
    class Meta:
        model=TA_Resource
        fields="__all__"
    
# Form to save one VM candidate in /add_vm url
class VmCandidateForm(forms.ModelForm):
    class Meta: 
        model = VmResource
        fields = "__all__"

class Ta_ResumeForm(forms.ModelForm):
    class Meta:
        model=Ta_resume
        fields="__all__"