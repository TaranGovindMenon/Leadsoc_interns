from django.db import models
from datetime import datetime
# Create your models here.

class Customer(models.Model):
    cName = models.CharField(max_length=50,primary_key=True)
    cEmail = models.EmailField(null=True)
    cUrl = models.CharField(max_length=50,null=True)
    
    class Meta:     
        db_table = "customer"

    def __str__(self):
        return str(self.cName)
    
class Buhead(models.Model):
    Bu_head_name=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.Bu_head_name

class SalesIncharge(models.Model):
    incharge_name=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.incharge_name

class Role(models.Model):
    role_name=models.CharField(max_length=100,primary_key=True)

    def __str__(self):
        return self.role_name
    

class Employee(models.Model):
    e_id=models.CharField(max_length=100,primary_key=True)
    eFname = models.CharField(max_length=50,null=True)
    eLname = models.CharField(max_length=50,null=True)
    refer_Customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    eEmail = models.EmailField(max_length=200,null=True)
    ePhone = models.CharField(max_length=50,unique=True)
    eExperience = models.IntegerField(default=0,null=True)
    eskills = models.CharField(max_length=100,null=True)
    eRole = models.ForeignKey(Role,on_delete=models.CASCADE) # designation
    eMP_Type = models.CharField(max_length=30,null=True) # either sales,software engineer, account
    estatus = models.CharField(max_length=100,null=True) # either free or deployed
    leadsoc_joining_date = models.DateField(null=True)
    customer_start_date = models.DateField(null=True)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return str(self.eFname)
         

class Emp_Experience(models.Model):
    # e_id=models.CharField(max_length=15,null=True)
    e_id=models.CharField(max_length=5)
    refer_customer=models.CharField(max_length=100,null=True)
    customer_start_date=models.DateField(null=True)
    customer_end_date=models.DateField(null=True)

        

class Customer_Requirements(models.Model):

    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)
    Customer_Requirement_id = models.IntegerField(primary_key=True)
    Required_skills = models.TextField()
    Job_Description = models.TextField()
    Required_Experience = models.FloatField(default=0)
    Open_positions = models.IntegerField(default=0)
    remain_positions = models.IntegerField(default=0)
    Position_Status = models.CharField(max_length=10) # active or closed        
    Sales_Incharge = models.ForeignKey(SalesIncharge, on_delete=models.CASCADE)# name of the person
    #Candidate_List = models.CharField(max_length=100,null=True) # need candidate list
    Bu_head=models.ForeignKey(Buhead,on_delete=models.CASCADE)
    Bu_remarks = models.CharField(max_length=1000,null=True, default="")

    class Meta:
        db_table = "customer_requirements"

    def __str__(self):
        return str(self.customers)
    
class CandidateList(models.Model):
    candidate_name = models.CharField(max_length=100,default="",editable=False,primary_key=True)
    interview_status = models.CharField(max_length=100,null=True)
    
    class Meta:
        db_table = "candidate_list"
    
    def __str__(self):
        return self.candidate_name

class addEmpToCustomer(models.Model):
    req_id=models.IntegerField()
    eFname = models.CharField(max_length=100,null=True)
    eLname = models.CharField(max_length=100, null=True)
    eskills = models.CharField(max_length=100,null=True)
    refer_Customer = models.ForeignKey(Customer, on_delete = models.CASCADE)
    estatus = models.CharField(max_length=100,null=True)
    empstatus = models.CharField(max_length=100,null=True, default='')
    comp_name = models.CharField(max_length=100,null=True)
    added_date = models.DateField(null=True)
    #empremarks = models.CharField(max_length=1000,null=True, default="")
    # ta_remarks = models.CharField(max_length=1000,null=True, default="")
    # sales_remarks = models.CharField(max_length=1000,null=True, default="")
    class Meta:
        db_table = "addemptocustomer"

    def __str__(self):
        return str(self.eFname)


class empRemarks(models.Model): 
    refer_addemp = models.ForeignKey(addEmpToCustomer, on_delete = models.CASCADE)
    remark_date = models.DateField(null=True)
    remarks = models.CharField(max_length=1000,null=True, default="")
    cname = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = "empRemarks"
        
    def __str__(self):
        return str(self.refer_addemp.eFname)
    
    

class Bu_Remarks(models.Model):
    refer_emp = models.ForeignKey(Employee, on_delete = models.CASCADE)
    cust_id = models.IntegerField()
    remark_date = models.DateField(null=True)
    remarks = models.CharField(max_length=1000,null=True, default="")
    class Meta:
        db_table = "Bu_remarks"
        
    def __str__(self):
        return str(self.cust_id)




class Employee_Details(models.Model):
    pass

class UploadFile(models.Model):
    specifications = models.FileField(upload_to='router_specifications')
    
class Login(models.Model):
    UserName = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    
    class Meta:
        db_table = "login"

