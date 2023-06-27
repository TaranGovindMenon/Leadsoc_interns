from import_export import resources
from .models import Employee,Customer

class EmployeeResource(resources.ModelResource):
    class Meta:
        model =Employee

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer