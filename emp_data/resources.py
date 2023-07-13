from import_export import resources
from .models import Employee,Customer

class EmployeeResource(resources.ModelResource):
    class Meta:
        model =Employee
        exclude=('id',)

class CustomerResource(resources.ModelResource):
    class Meta:
        model = Customer