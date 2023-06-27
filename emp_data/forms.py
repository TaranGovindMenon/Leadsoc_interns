from django import forms
from emp_data.models import Employee
from emp_data.models import Customer
from emp_data.models import Login
from emp_data.models import Customer_Requirements
from emp_data.models import addEmpToCustomer
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
    
