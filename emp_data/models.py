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
    
# class Buhead(models.Model): #Just has the names.. can use employee model to sort it 
#     Bu_head_name=models.CharField(max_length=100,primary_key=True)
#     def __str__(self):
#         return self.Bu_head_name

# class SalesIncharge(models.Model):
#     incharge_name=models.CharField(max_length=100,primary_key=True)

#     def __str__(self):
#         return self.incharge_name

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
    #eMP_Type = models.CharField(max_length=30,null=True) # either sales,software engineer, account
    estatus = models.CharField(max_length=100,null=True) # either free or deployed
    leadsoc_joining_date = models.DateField(null=True)
    customer_start_date = models.DateField(null=True)

    class Meta:
        db_table = "employee"

    def __str__(self):
        return str(self.eFname)
         
from datetime import datetime

class Emp_Experience(models.Model):
    # e_id=models.CharField(max_length=15,null=True)
    e_id=models.CharField(max_length=5)
    refer_customer=models.CharField(max_length=100,null=True)
    customer_start_date=models.DateField(null=True)
    customer_end_date=models.DateField(null=True)
    
    @property
    def duration(self):
        return (self.customer_end_date-self.customer_start_date).days

        

class Customer_Requirements(models.Model):
    customers = models.ForeignKey(Customer, on_delete = models.CASCADE)
    Customer_Requirement_id = models.IntegerField(primary_key=True)
    Required_skills = models.TextField()
    Job_Description = models.TextField()
    Required_Experience = models.FloatField(default=0)
    Open_positions = models.IntegerField(default=0)
    remain_positions = models.IntegerField(default=0)
    Position_Status = models.CharField(max_length=10) # active or closed        
    Sales_Incharge = models.CharField(max_length=50,null=True)# name of the person
    #Candidate_List = models.CharField(max_length=100,null=True) # need candidate list
    Bu_head=models.CharField(max_length=50,null=True)
    #Bu_remarks = models.CharField(max_length=1000,null=True, default="")

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

class addEmpToCustomer(models.Model):# add two more fields: source (leadsoc,TA,VM), source_id
    req_id=models.IntegerField() #Model name change: Employee requirement 
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
    #cname = models.CharField(max_length=100,null=True)
    remark_author = models.CharField(max_length=100,null=True)
    class Meta:
        db_table = "empRemarks"
        
    def __str__(self):
        return str(self.refer_addemp.eFname)
    
    

class Remarks(models.Model):
    refer_emp = models.ForeignKey(Employee, on_delete = models.CASCADE)
    cust_requirement_id = models.IntegerField()
    remark_date = models.DateField(null=True)
    remarks = models.CharField(max_length=1000,null=True, default="")
    class Meta:
        db_table = "Bu_remarks"
        
    def __str__(self):
        return str(self.cust_requirement_id)




class Employee_Details(models.Model):
    pass

class UploadFile(models.Model):
    specifications = models.FileField(upload_to='router_specifications')
    
class Login(models.Model):
    UserName = models.CharField(max_length=50)
    password = models.CharField(max_length=32)
    
    class Meta:
        db_table = "login"

class TA_Resource(models.Model):
    ta_id = models.CharField(max_length=10,unique=True)
    archived = models.CharField(max_length=100)
    date = models.DateField()
    name = models.CharField(max_length=300)
    BU = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    skillset = models.CharField(max_length=500)
    education = models.CharField(max_length=500)
    experience = models.FloatField()
    relevant_exp = models.FloatField()
    current_org = models.CharField(max_length=500)
    current_ctc = models.FloatField()
    expected_ctc = models.FloatField()
    actual_notice_period = models.IntegerField()
    notice_period = models.IntegerField()
    current_loc = models.CharField(max_length=500)
    preferred_loc = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=15,primary_key=True)
    email = models.EmailField()
    status = models.CharField(max_length=100)
    BU_comments = models.CharField(max_length=1000)
    TA_comments = models.CharField(max_length=1000)
    comment_by_prerana = models.CharField(max_length=500)
    T1_panel = models.CharField(max_length=100)
    T1_IW_date = models.DateField()
    T2_panel = models.CharField(max_length=100)
    T2_IW_date = models.DateField()
    source = models.CharField(max_length=500)
    Rec_prime = models.CharField(max_length=500)
    Domain = models.CharField(max_length=100)
    T1 = models.CharField(max_length=100)
    T2 = models.CharField(max_length=100)
    # resume = models.FileField()