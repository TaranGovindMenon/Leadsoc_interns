from ctypes import wstring_at
from pkgutil import get_data
import queue
import quopri
from django.shortcuts import render,redirect,get_object_or_404
from emp_data.models import Customer,Employee,Customer_Requirements, Remarks, empRemarks
from .resources import EmployeeResource
from emp_data.forms import CustomerForm,EmployeeForm, addEmpToCustomerForm,loginForm,UploadFileForm,Customer_RequirementForm,TA_Form, VmCandidateForm
from django.contrib import messages
from django.contrib.auth.models import auth
from emp_data.models import *
from tablib import Dataset
from .models import Customer
from django.template import loader
import xlwt
from django.http import HttpResponse
from django.db.models import Q
from datetime import date

def loginCheck(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return redirect("/emp")
        else:
            messages.info(request, 'invalid credentials')
            return redirect("/emp")



    else:
        form = loginForm()
        return render(request, "regsitration/login.html")



#Home page
def home(request):
    return render(request,"home.html")
'''
def admin_login(request):
    return render(request, 'admin_login.html')
'''
# To add Customer

def comp(request):
    if request.method == "POST":

        form = CustomerForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Company Details saved successfully')
                return redirect("/show")
            except:
                pass
    else:
        form = CustomerForm()
    return render(request, "index.html", {'form':form})


# add company details
'''
def comp(request):
    if request.method == "POST":
        print("Hi Anil")
        cName = request.POST['cName']
        cEmail = request.POST['cEmail']
        cLogo = request.POST['cLogo']
        cUrl = request.POST['cUrl']
        ins=Customer(cName=cName,cEmail=cEmail,cLogo=cLogo,cUrl=cUrl)
        ins.save()

        print(cName)
    return render(request, 'index.html')
'''

def emp(request):
    form=EmployeeForm()
    if request.method == "POST":
        '''eFname = request.POST['eFname']
        eLname = request.POST['eLname']
        refer_Customer_no = request.POST['refer_Customer']
        eEmail = request.POST['eEmail']
        ePhone = int(request.POST['ePhone'])
        eExperience =request.POST['eExperience']
        eskills = request.POST['eskills']
        eRole = request.POST['eRole']
        eMP_Type = request.POST['eMP_Type']
        estatus = request.POST['estatus']
        leadsoc_joining_date = request.POST['leadsoc_joining_date']
        customer_start_date = request.POST['customer_start_date']
        remarks = request.POST['remarks']
        ins=Employee(eFname=eFname, eLname=eLname, refer_Customer_id=refer_Customer_no, eEmail=eEmail, ePhone=ePhone, 
                     eExperience=eExperience,eskills=eskills,eRole=eRole,eMP_Type=eMP_Type,estatus=estatus,
                     leadsoc_joining_date=leadsoc_joining_date,customer_start_date=customer_start_date,remarks=remarks)
        ins.save()'''
        form=EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Details Saved !")
        # erole=form.cleaned_data['eRole']
        emp_name=request.POST.get('eFname',False)
        erole=request.POST.get('eRole',False)
        # ePhone=request.POST.get('ePhone',False)
        if (request.POST.get('estatus')=='Free'):
            candidate_instance=CandidateList(candidate_name=emp_name,interview_status='Rejected')
            candidate_instance.save()
            return redirect(f'/showemp')
        # if erole=='Bu Head':
        #     # return HttpResponse('Bu Head')
        #     instance=Buhead(Bu_head_name=emp_name)
        #     instance.save()
        #     return redirect(f'/showemp')

        # if erole=='Sales Incharge':
        #     # return HttpResponse('Sales Incharge')
        #     instance=SalesIncharge(incharge_name=emp_name)
        #     instance.save()
        #     return redirect(f'/showemp')


        # return redirect('/showemp')
        else:
            return HttpResponse(form.errors)
    
    else:
        list=Customer.objects.all()
        role=Role.objects.all()
        list1=[]
        rolelist=[]
        for item in list:
            list1.append(item.cName)
        for item in role:
            rolelist.append(item.role_name)


        return render(request, 'addemp.html',{'zipped_lists': list1,'rolelist':rolelist,'status':['Free','Deployed','Support Team']})


def experience(request,e_id):
    instance=Employee.objects.get(pk=e_id)
    first_name=instance.eFname
    last_name=instance.eLname
    name=first_name + " " + last_name
    custom=Customer.objects.all()
    today = date.today().strftime("%Y-%m-%d")
    customerlist=[]
    for item in custom:
        customerlist.append(item.cName)
    return render(request,'experience.html',{'e_id':e_id,'name':name,'customerlist':customerlist, 'today': today})



def addexperience(request, e_id):
    if request.method == 'POST':
        c_name = request.POST.getlist('refer_customer')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        instance=Emp_Experience(e_id=e_id,refer_customer=c_name[0],customer_start_date=start_date,customer_end_date=end_date)
        instance.save()
        return redirect('/showemp')
    else:
        return HttpResponse("Error")
    # num_entries=len(request.POST.getlist('refer_customer[]'))
    # name=request.POST.getlist('refer_customer[]')
    # start=request.POST.getlist('customer_start_date[]')
    # end=request.POST.getlist('customer_end_date[]')
    # for i in range(num_entries):
    #     c_name=name[i]
    #     s_date=start[i]
    #     e_date=end[i]
    #     instance=Emp_Experience(e_id=e_id,refer_customer=c_name,customer_start_date=s_date,customer_end_date=e_date)
    #     instance.save()
    # return redirect('/showemp')

def delete_experience(request, exp_id): 
    exp_instance = Emp_Experience.objects.get(id=exp_id)
    exp_instance.delete()
    return redirect('/showemp')


def add_cust_requirements(request):
    form=Customer_RequirementForm()
    if request.method == "POST":
        
        '''Requirement_Id = request.POST['Requirement_Id']
        customers = request.POST['customers']
        Customer_Requirement_id = request.POST['Customer_Requirement_id']
        Required_skills = request.POST['Required_skills']
        Job_Description = request.POST['Job_Description']
        Required_Experience =request.POST['Required_Experience']
        Open_positions = request.POST['Open_positions']
        remain_positions = request.POST['remain_positions'] 
        Position_Status = request.POST['Position_Status']        
        Sales_Incharge = request.POST['Sales_Incharge']
        bu_head = request.POST['Bu_head']        
        cust_require_data=Customer_Requirements(Requirement_Id=Requirement_Id,customers_id=customers,Customer_Requirement_id=Customer_Requirement_id, 
                                                Required_skills=Required_skills, Job_Description=Job_Description, Required_Experience=Required_Experience,
                                                   Open_positions =Open_positions, remain_positions=remain_positions, Position_Status=Position_Status,
                                                    Sales_Incharge=Sales_Incharge, Bu_head=bu_head)
        cust_require_data.save()'''
        form=Customer_RequirementForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Details Saved !')
            return redirect('/show_cust_requirements')
        else:
            return HttpResponse(form.errors)

    else:
        list1=Customer.objects.all()
        list2=Employee.objects.filter(eRole='Bu Head')
        list3=Employee.objects.filter(eRole='Sales Incharge')
        customerlist=[]
        bulist=[]
        saleslist=[]
        for item in list1:
            customerlist.append(item.cName)
        for item in list2:
            bulist.append(item.eFname)
        for item in list3:
            saleslist.append(item.eFname)
        return render(request, 'addcustrequirements.html',{'customerlist': customerlist, 'bulist': bulist, 'saleslist' : saleslist})

# To retrieve Customer details

def update_cust_requirements(request,Customer_Requirement_id):
    # model_instance=get_object_or_404(Customer_Requirements, pk=Requirement_id) 
    model_instance=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
    model_instance.Required_skills=request.POST['Required_skills']
    model_instance.Job_Description=request.POST['Job_Description']
    model_instance.Required_Experience=request.POST['Required_Experience']
    model_instance.Open_positions=request.POST['Open_positions']
    model_instance.remain_positions=request.POST['Open_positions']
    model_instance.Position_Status=request.POST['Position_Status']
    model_instance.Sales_Incharge=request.POST['Sales_Incharge']
    model_instance.Bu_head = request.POST['Bu_Head']
    model_instance.save()
    return redirect('/show_cust_requirements')  
    
    
    if request.method=='POST':
        form=Customer_RequirementForm(request.POST,instance=model_instance)
        if form.is_valid():
            form.save()
    return redirect('/show_cust_requirements')    

def show(request):
    if not request.user.is_authenticated:
        return redirect('home')
    companies = Customer.objects.all()
    return render(request, "show.html", {'companies':companies})

# To Edit Customer details
# def edit(request, cName):
#     if not request.user.is_authenticated:
#         return redirect('home')
#     customer = Customer.objects.get(cName=cName)
#     return render(request, "edit.html", {'customer':customer})

# To Update Customer
def update(request, cName):
    if not request.user.is_authenticated:
        return redirect('home')
    customer = get_object_or_404(Customer,pk=cName)
    form = CustomerForm(request.POST or None, instance= customer)
    if form.is_valid():
         form.save()
         return redirect("/show")
    else:
        return HttpResponse(form.errors)
    
    # return render(request, "edit.html", {'customer': customer})

# To Delete Customer details
def delete(request, cName):
    if not request.user.is_authenticated:
        return redirect('home')
    
    customer = Customer.objects.get(cName=cName)
    customer.delete()    
    messages.success(request,'The Selected customer'  + str(customer.cName) +  'is deleted successfully')
   
    return redirect("/show")


# from django.db.models import Q

# def show_cust_requirements(request):
#     customer_requirements = Customer_Requirements.objects.all()
#     form = Employee.objects.filter(estatus='Free').values()
#     if request.method == "GET":
#         skills = request.GET.get('searchskill')
#         if skills:
#             form = Employee.objects.filter(Q(eskills__icontains=skills) & Q(estatus='Free'))
#         else:
#             form = Employee.objects.filter(estatus='Free')
#     return render(request, "show_cust_requirements.html", {'customer_requirements': customer_requirements, 'form': form})


def show_cust_requirements(request):
    if not request.user.is_authenticated:
        return redirect('home')
    else :
        customer_requirements = Customer_Requirements.objects.all()
        #saleslist=SalesIncharge.objects.all()
        all_remarks = Remarks.objects.all()
        current_user = request.user.username.title()
        sales_incharge = Employee.objects.filter(eRole="Sales Incharge")
        bu_head = Employee.objects.filter(eRole="Bu Head")
        return render(request,'show_cust_requirements.html',{'customer_requirements':customer_requirements,'remarks':all_remarks, 
                                                             'sales_incharge': sales_incharge, 'bu_head': bu_head, 'current_user':current_user,
                                                             'bu_select':'Choose', "sales_select":'Choose', 'status_select':'Choose'})

def filtered_cust_requirements(request,bu,sales,st):
    # buhead=request.GET.get('arg1')
    # salesincharge=request.GET.get('arg2')
    # status=request.GET.get('arg3')
    if bu=='All':
        customer_requirements=Customer_Requirements.objects.filter(Sales_Incharge=sales,Position_Status=st)
    elif sales=='All':
        customer_requirements=Customer_Requirements.objects.filter(Bu_head=bu,Position_Status=st)
    else:
        customer_requirements=Customer_Requirements.objects.filter(Bu_head=bu,Sales_Incharge=sales,Position_Status=st)
    all_remarks = Remarks.objects.all()
    bu_head = Employee.objects.filter(eRole="Bu Head")
    current_user = request.user.username.title() 
    sales_incharge= Employee.objects.filter(eRole="Sales Incharge")
    return render(request,'show_cust_requirements.html',{'customer_requirements':customer_requirements,'remarks':all_remarks, 
                                                        'sales_incharge': sales_incharge, 'bu_head': bu_head, 'current_user':current_user,'bu_select': bu, "sales_select": sales, 'status_select': st})

def remarks(request, cust_requirement_id):
    if request.method == 'POST':
        current_user = request.user.username.title()
        remark_text = request.POST.get('remark_text', '')
        today = date.today()
        emp = Employee.objects.get(eFname = current_user)
        new_remark = Remarks(refer_emp = emp, remarks=remark_text, remark_date=today, cust_requirement_id=cust_requirement_id)
        new_remark.save()
        # model_instance = Customer_Requirements.objects.get(Customer_Requirement_id=cust_id)
        # model_instance.Bu_remarks = request.POST.get('BU_remark_text', '')
        # model_instance.save()
        
        return redirect('/show_cust_requirements')

def cust_req_dropdown(request, ref): 
    if ref[:1] == 'P':
        cust = Customer_Requirements.objects.get(pk=ref[2:3])
        if ref[1:2] == 'A': 
            cust.Position_Status = 'Active'
        elif ref[1:2] == 'H': 
            cust.Position_Status = 'Hold'
        elif ref[1:2] == 'I': 
            cust.Position_Status = 'Inactive'
    elif ref[:1] == 'S':
        cust = Customer_Requirements.objects.get(pk=ref[1:2])
        cust.Sales_Incharge = ref[2:]
    elif ref[:1] == 'B': 
        cust = Customer_Requirements.objects.get(pk=ref[1:2])
        cust.Bu_head = ref[2:]
    cust.save()
    return redirect('/show_cust_requirements')
    

def summary(request):
    first=Employee.objects.filter(eRole="Bu Head")
    second=Employee.objects.filter(eRole="Sales Incharge")
    saleslist=[]
    bulist=[]
    for val in first:
        bulist.append(val.eFname)
    for val in second:
        saleslist.append(val.eFname)
    final=[]
    for val in saleslist:
        firstarray=[]
        for newval in bulist:
            customercount=len(Customer_Requirements.objects.filter(Bu_head=str(newval),Sales_Incharge=str(val)))
            firstarray.append(customercount)
        firstarray.append(sum(firstarray))
        firstarray.insert(0,val)
        final.append(firstarray)
    length=len(bulist)
    context={'final':final,
             'bulist':bulist,
             'length':length}
    return render(request,'summary.html',context)
        

def add_ta(request):
    form=TA_Form()
    if request.method=='POST':
        form=TA_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/show_ta')
        else:
            return HttpResponse(form.errors)
    else:
        return render(request,'addTA.html')

def show_ta(request):
    ta_instance=TA_Resource.objects.all()
    return render(request,'showTa.html',{'ta_instance':ta_instance})

def delete_ta(request,phone_number):
    instance=TA_Resource.objects.get(pk=phone_number)
    instance.delete()
    return redirect('/show_ta')





# def sample_view(request):
#     current_user = request.user
#     return HttpResponse(current_user.username)

    # form = Employee.objects.filter(estatus ='Free').values()
    # if request.method == "GET":   
    #     free = Employee.objects.filter(estatus ='Free').values()              
    #     skills = request.GET.get('searchskill')
    #     #f = Employee.objects.values_list('eskills')
    #     if skills == free:  
    #     #if skills != f:
    #         form = Employee.objects.filter(eskills__icontains= skills).filter(estatus__icontains= free)
    #         #above eskills form column name with double underscore icontain inbuilt attribute
    # return render(request, "show_cust_requirements.html", {'customer_requirements':customer_requirements, 'form': form})


# show customer_requirements details
'''
def show_cust_requirements(request):
    if not request.user.is_authenticated:
        return redirect('login')
    customer_requirements = Customer_Requirements.objects.all()
    return render(request, "show_cust_requirements.html", {'customer_requirements':customer_requirements})
'''
def job_description(request):
    job_desc = Customer_Requirements.objects.values('Job_Description')
    #print(job_desc)
    return render(request,"job_description.html",{'job_desc':job_desc})

# adding candidate details in customer_requirement page
def add_candidate(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        candidate_name = request.POST['candidate_name']
        interview_status = request.POST['interview_status']
        candidate_data  = CandidateList(candidate_name=candidate_name,interview_status=interview_status)
        candidate_data.save()        
        return redirect("/show_candidate.html")
    else:
        return render(request,"add_candidates.html")
'''
def show_candidate(request):
    candidate = CandidateList.objects.all()
    return render(request,"show_candidate.html",{'candidate':candidate})'''
'''
def show_candidate(request):
    candidate = Employee.objects.filter(estatus ='Free').values()
    return render(request,"show_candidate.html",{'candidate':candidate})'''
# search and show the data

def show_candidate(request,customers,Customer_Requirement_id):

    form = Employee.objects.filter(estatus ='Free').values()
    #form = Employee.objects.all()
    if request.method == "GET":   
        free = Employee.objects.filter(estatus ='Free').values()              
        skills = request.GET.get('searchskill')      
        #f = Employee.objects.values_list('eskills')
        if skills != None: 
        #if skills == free:
            form = Employee.objects.filter(eskills__icontains= skills,estatus='Free')
            #above eskills form column name with double underscore icontain inbuilt attribute
    choice=1
    return render(request,'show_candidate.html',{'form':form , 'customer_name':customers,'Customer_Requirement_id':Customer_Requirement_id,'choice':choice})

def show_talist(request,customer_name,Customer_Requirement_id):
    form=TA_Resource.objects.filter(status='Selected').values()
    if request.method=='GET':
        skills=request.GET.get('searchskill')
        if skills != None:
            form=TA_Resource.objects.filter(skillset__icontains=skills)
    choice=2
    return render(request,'show_ta_candidate.html',{'form':form,"customer_name":customer_name,"Customer_Requirement_id":Customer_Requirement_id,'choice':choice})

def show_vmlist(request,customer_name,Customer_Requirement_id):
    form=VmResource.objects.filter(interview_status='Selected').values()
    if request.method=='GET':
        skills=request.GET.get('searchskill')
        if skills!=None:
            form=VmResource.objects.filter(skillset__icontains=skills)
    choice=3
    return render(request,'show_vm_candidate.html',{'form':form,'customer_name':customer_name,'Customer_Requirement_id':Customer_Requirement_id,'choice':choice})

def checkbox(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        if request.POST.getlist('checks'):
            
            s = request.POST.getlist('checks')
            print(s)
            for i in s:               
                savedata = addEmpToCustomer()
                savedata.eFname = i
                savedata.save()         
            

        return redirect('/showEmpToCustomer')
    else:
        return redirect('showEmpToCustomer')


from .forms import addEmpToCustomerForm

# def addempcustomer(request):
#     if not request.user.is_authenticated:
#         return redirect('home')
#     form=addEmpToCustomerForm()
#     if request.method == 'POST':        
#         form = addEmpToCustomerForm(request.POST)
#         if form.is_valid():
#             form.save()         
#             return redirect('/showEmpToCustomer')
#     context = {'form': form}
#     return render(request, 'showEmpToCustomer.html', context)


def savedvalues(request,customer_name,Customer_Requirement_id,choice):

    
    if request.method == 'POST':
        if choice==1:
            emp = request.POST.getlist('eFname')
            print(emp)
            savedata1 = addEmpToCustomer()
            emp1=[]
            today = date.today()
            for i in emp:
               newval=Employee.objects.get(eFname=i)
               newval.estatus='Deployed'
               newval.save()
               final=addEmpToCustomer(req_id=Customer_Requirement_id,eFname=newval.eFname + " " + newval.eLname,eskills=newval.eskills,refer_Customer=Customer(cName=customer_name),estatus='Deployed', comp_name= customer_name, added_date=today)
               final.save()
               newval2=addEmpToCustomer.objects.filter(eFname=i)
               emp1.append(newval2)
        elif choice==2:
            emp = request.POST.getlist('name')
            print(emp)
            savedata1 = addEmpToCustomer()
            emp1=[]
            today = date.today()
            for i in emp:
               newval=TA_Resource.objects.get(name=i)
               newval.estatus='Deployed'
               newval.save()
               final=addEmpToCustomer(req_id=Customer_Requirement_id,eFname=newval.name,eskills=newval.skillset,refer_Customer=Customer(cName=customer_name),estatus='Deployed',empstatus='Selected',comp_name= customer_name, added_date=today)
               final.save()
               requirement_instance=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
               requirement_instance.remain_positions-=1
               requirement_instance.save()
               newval2=addEmpToCustomer.objects.filter(eFname=i)
               emp1.append(newval2)
        elif choice==3:
            emp = request.POST.getlist('candidate_name')
            print(emp)
            savedata1 = addEmpToCustomer()
            emp1=[]
            today = date.today()
            for i in emp:
               newval=VmResource.objects.get(candidate_name=i)
               final=addEmpToCustomer(req_id=Customer_Requirement_id,eFname=newval.candidate_name,eskills=newval.skillset,refer_Customer=Customer(cName=customer_name),estatus='Deployed',empstatus='Selected', comp_name= customer_name, added_date=today)
               final.save()
               requirement_instance=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
               requirement_instance.remain_positions-=1
               requirement_instance.save()
               newval2=addEmpToCustomer.objects.filter(eFname=i)
               emp1.append(newval2)

        
        # return HttpResponse(emp1)
    #         savedata2=Employee.objects.get(eFname=val)
    #         savedata1=addEmpToCustomer(eFname=savedata2.eFname,eLname=savedata2.eLname,eskills=savedata2.eskills,refer_Customer=10,estatus='deployed')
    #         savedata1.save()
    #         # emp.append(savedata2)
    #     # savedata.eFname=request.POST.getlist('eFname')
    #     # savedata.save()
        else:
            return HttpResponse("Sorry Buddy")  
    return redirect(f'/showEmpToCustomer/{customer_name}/{Customer_Requirement_id}')

#show added employe to customer
def showEmpToCustomer(request, cust_name,Customer_Requirement_id):  
    if not request.user.is_authenticated:
        return redirect('home')
    emp_data = addEmpToCustomer.objects.filter(req_id=Customer_Requirement_id)
    req_instance=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
    position=req_instance.remain_positions
    empremarks = empRemarks.objects.all()
    #return HttpResponse(empremarks.remark_date)
    return render(request, "showEmpToCustomer.html", {'form':emp_data,'Customer_Requirement_id':Customer_Requirement_id,'position':position,
    'cust_name': cust_name, 'remarks': empremarks})



def emp_remarks(request, eFname):
    if request.method == 'POST':
        current_user = request.user.username.title()
        emp = addEmpToCustomer.objects.get(eFname=eFname)
        remark_text = request.POST.get('remark_text', '')
        today = date.today()
        emp = addEmpToCustomer.objects.get(eFname = eFname)
        new_remark = empRemarks(refer_addemp=emp, remark_date=today, remarks=remark_text, remark_author=current_user)
        new_remark.save()
        return redirect(f'/showEmpToCustomer/{emp.comp_name}/{emp.req_id}')
        # cname = model_instance.comp_name
        # if eFname[:2] == 'BU':
        #     model_instance.bu_remarks = request.POST.get('BU_remark_text', '')
        # elif eFname[:2] == 'TA':
        #     model_instance.ta_remarks = request.POST.get('TA_remark_text', '')
        # elif eFname[:2] == 'SL':
        #     model_instance.sales_remarks = request.POST.get('SL_remark_text', '')
        # model_instance.save()
    #return redirect(f'/showEmpToCustomer/{cname}')


def selection_status(request, status,Customer_Requirement_id): 
    model_instance = addEmpToCustomer.objects.get(eFname=status[2:])
    requirement_instance=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
    cname = model_instance.comp_name
    #if request.method == 'POST':
        #model_instance = addEmpToCustomer.objects.get(eFname=status[2:])
    if status[:2] == 'SL':
        model_instance.empstatus = 'Selected'

        requirement_instance.remain_positions-=1
        model_instance.save()
        requirement_instance.save()

        #return HttpResponse('something in it')
    elif status[:2] == 'RJ': 
        model_instance.empstatus = 'Rejected'
        model_instance.save()   
        #return HttpResponse('something else in it')
    # else: 
    #     return HttpResponse('none')
    elif status[:2]=='BU':
        model_instance.empstatus='Shortlisted by BU'
        model_instance.save()
    elif status[:2]=='CL':
        model_instance.empstatus='Shortlisted by Client'
        model_instance.save()
    elif status[:2]=='OP':
        model_instance.empstatus='Onboarding Progress'
        model_instance.save()
    elif status[:2]=='OB':
        model_instance.empstatus='Onboarded'
        model_instance.save()
    elif status[:2]=='RR':
        model_instance.empstatus='Resume Rejected'
        model_instance.save()
    return redirect(f'/showEmpToCustomer/{cname}/{Customer_Requirement_id}')

# To display all the VM candidates 
def show_vm(request):
    all_vm_candidates = VmResource.objects.all()
    return render(request, "show_vm_candidates.html", {"candidate_list":all_vm_candidates})

# Form to add only one VM candidate 
def add_vm(request): 
    if request.method == "POST":
        form=VmCandidateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Details Saved !")
            return redirect("/show_vm")
    return render(request, "add_vm_candidates.html")

def update_vm_candidates(request): 
    pass

# To upload data containing VM candidates
def vm_data_upload(request): 
    if request.method == "POST":
        dataset = Dataset()
        new_vm = request.FILES['myfile']
        if not new_vm.name.endswith('xlsx'):
            messages.info(request, 'Wrong format of file')
            return render(request, 'upload_vm_candidates.html')
        imported_data = dataset.load(new_vm.read(), format='xlsx')
        for data in imported_data:
            value = VmResource(
                position_status=data[0],
                pr_date=data[1],
                vendor_name=data[2],
                candidate_source=data[3],
                candidate_name=data[4],
                skillset=data[5],
                experience=data[6],
                education=data[7],
                billing_rate=data[8],
                bu_head=data[9],
                location=data[10],
                notice_period=data[11],
                reviewer_name=data[12],
                remarks_panel=data[13],
                vm_comment=data[14],
                client_name=data[15],
                interview_schedule=data[16],
                interview_status=data[17],
                comments=data[18],
                remarks=data[19],
                email=data[20],
                phone_number=data[21],
                mode=data[22]
            )
            value.save()
        return redirect("/show_vm")
    return render(request, "upload_vm_candidates.html")



#dropdown customer names
def dropDownCustomer(request):
    if request.method == "POST":
        if request.POST.get('cName'):
            savevalue = addEmpToCustomer()
            savevalue.refer_Customer = request.POST.get('cName')
            savevalue.save()
            messages.success(request,'The Selected customer' +savevalue.refer_Customer+ 'is saved successfully')
            return redirect('/showEmpToCustomer')
        
        else:
            return render(request,'showEmpToCustomer')
        
def showDropDown(request):
    display_cust = addEmpToCustomer.objects.all()

    return render(request,'showEmpToCustomer.html',{'display_cust':display_cust})

# delete employee from addEmpToCustomer table

def delete_Emp_Customer(request,eFname,Customer_Requirement_id):   
    req=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
    if not request.user.is_authenticated:
        return redirect('home') 
    try:
        emp = addEmpToCustomer.objects.get(eFname=eFname)
        try:
            status_instance=Employee.objects.get(eFname=eFname)
            status_instance.estatus='Free'
            status_instance.save()
        except:
            pass
        emp.delete()
        req.remain_positions+=1
        req.save()
    except addEmpToCustomer.MultipleObjectsReturned:
        emp = addEmpToCustomer.objects.filter(eFname=eFname)[0]
        emp.delete()
        status_instance=Employee.objects.get(eFname=eFname)[0]
        status_instance.estatus='Free'
        status_instance.save()
        req=Customer_Requirements.objects.get(pk=Customer_Requirement_id)
        req.remain_positions+=1
        req.save()

    messages.success(request,'The Selected Employee'  + emp.eFname +  'is deleted successfully')
    company=req.customers
    return redirect(f'/showEmpToCustomer/{company}/{Customer_Requirement_id}')


  
  
  
# To create employee
'''
def emp(request):
    if request.method == "POST":
        
        form = EmployeeForm(request.POST)
        if form.is_valid():
            
            try:
                form.save()
                return redirect("/showemp.html")
            except:
                pass
    else:
        
        form = EmployeeForm()
        
    return render(request, "addemp.html", {'form':form})
'''

# To show employee details
def showemp(request):
    if not request.user.is_authenticated:
        return redirect('home')
    employees = Employee.objects.all()
    current_user = request.user.username.title()
    current_emp = Employee.objects.get(eFname=current_user)
    customerlist=Customer.objects.all()
    experiencelist=Emp_Experience.objects.all()
    rolelist=Role.objects.all()
    add_exp_btn = True
    return render(request, "showemp.html", {'employees':employees,'customerlist':customerlist,'experiencelist':experiencelist,'rolelist':rolelist,'statuslist':['Free','Deployed','Support Team'], 'current_emp': current_emp, 'add_exp_btn': add_exp_btn})

# To delete employee details
def deleteEmp(request, e_id):
    if not request.user.is_authenticated:
        return redirect('home')
    employee = Employee.objects.get(pk=e_id)
    employee.delete()
    return redirect("/showemp")

# To edit employee details
# def editemp(request, eFname):
#     if not request.user.is_authenticated:
#         return redirect('home')
#     employee = Employee.objects.get(eFname=eFname)
#     return render(request, "editemployee.html", {'employee':employee})

# To update employee details
def updateEmp(request, e_id):
    if not request.user.is_authenticated:
        return redirect('home')
    employee = Employee.objects.get(pk=e_id)
    if request.method=='POST':
        ref_name=employee.eFname

        employee.eFname=request.POST['eFname']
        employee.eLname=request.POST['eLname']
        employee.refer_Customer=Customer(cName=request.POST['refer_Customer'])
        employee.eEmail=request.POST['eEmail']
        newval=Role(role_name=request.POST['eRole'])
        # if str(employee.eRole)=='Bu Head' and str(newval.role_name)=='Sales Incharge':
        #     Bu_instance=Buhead.objects.filter(pk=ref_name)
        #     Bu_instance.delete()
        #     s_instance=SalesIncharge(incharge_name=employee.eFname)
        #     s_instance.save()
        #     employee.eRole=newval
        # if str(employee.eRole)=='Sales Incharge' and str(newval.role_name)=='Bu Head':
        #     s_instance=SalesIncharge.objects.filter(pk=ref_name)
        #     s_instance.delete()
        #     Bu_instance=Buhead(Bu_head_name=employee.eFname)
        #     Bu_instance.save()
        #     employee.eRole=newval
        employee.eRole=newval
        employee.estatus=request.POST['estatus']
        employee.save()

    return redirect("/showemp")

    # form = EmployeeForm(request.POST, instance= employee)
    
    # if form.is_valid():
        
    #     form.save()
        
    return render(request, "editemployee.html", {'employee': employee})

def save_emp_details(request): 
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        selected_employees = request.POST.getlist('employee_checkbox')
        for employee_id in selected_employees:
            employee = Employee.objects.get(id=employee_id)
            add_emp = addEmpToCustomer(
                eFname=employee.eFname,
                eLname=employee.eLname,
                refer_Customer=request.user.customer,  # Assuming you have a logged-in user with a related customer
                eskills=employee.eskills
            )
            add_emp.save()
    return redirect("/show_cust_requirements")


# this is working upload employee data to model
def simple_upload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_employee = request.FILES['myfile']

        if not new_employee.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'upload.html')
        
        imported_data = dataset.load(new_employee.read(), format='xlsx')
        for data in imported_data:
            #print(data[1])
            value = Employee(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                )
            value.save()
            if data[9]=='Free':
                newvalue=CandidateList(candidate_name=data[1],interview_status='Rejected')
                newvalue.save()
        return redirect("/showemp")
        
    return render(request,'upload.html')

# upload customer data to model
def customer_data_upload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_customer = request.FILES['myfile']

        if not new_customer.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'upload.html')
        
        imported_data = dataset.load(new_customer.read(), format='xlsx')
        for data in imported_data:
            print(data[1])
            value = Customer(
                data[0],
                data[1],
                data[2],                           
                )
            value.save()
        return redirect("/show")
    
    return render(request,'upload.html')

# upload customer requirement data the model
def customer_requirement_file(request):
    if not request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        
        #Employee_Resource = EmployeeResource()
        dataset = Dataset()
        new_Requirements = request.FILES['file']

        if not new_Requirements.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'customer_requirement_data.html')
        
        imported_data = dataset.load(new_Requirements.read(), format='xlsx')
        for data in imported_data:
            print(data[1])
            value = Customer_Requirements(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                #data[10]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
                )
            value.save()
        return redirect("/show_cust_requirements")
        
    return render(request,'customer_requirement_data.html')

#TA Upload Excel File Option
def ta_upload(request):
    if not request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        dataset=Dataset()
        new_details=request.FILES['file']

        if not new_details.name.endswith('xlsx'):
            messages.info(request,'Wrong format of file')
            return render(request,'showTA.html')
        imported_data = dataset.load(new_details.read(), format='xlsx')
        for data in imported_data:
            value=TA_Resource(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5],
                data[6],
                data[7],
                data[8],
                data[9],
                data[10],
                data[11],
                data[12],
                data[13],
                data[14],
                data[15],
                data[16],
                data[17],
                data[18],
                data[19],
                data[20],
                data[21],
                data[22],
                data[23],
                data[24],
                data[25],
                data[26],
                data[27],
                data[28],
                data[29],
                data[30],
                data[31],
                # data[32],
                )
            value.save()
        return redirect('/show_ta')
    

    return render(request,'TA_upload.html')




#Reset and login views

from urllib.parse import urlparse, urlunparse

from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

UserModel = get_user_model()


class RedirectURLMixin:
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    success_url_allowed_hosts = set()

    def get_success_url(self):
        return self.get_redirect_url() or self.get_default_redirect_url()

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name)
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""

    def get_success_url_allowed_hosts(self):
        return {self.request.get_host(), *self.success_url_allowed_hosts}

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        raise ImproperlyConfigured("No URL to redirect to. Provide a next_page.")


class LoginView(RedirectURLMixin, FormView):
    """
    Display the login form and handle the login action.
    """

    form_class = AuthenticationForm
    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                self.redirect_field_name: self.get_redirect_url(),
                "site": current_site,
                "site_name": current_site.name,
                **(self.extra_context or {}),
            }
        )
        return context


class LogoutView(RedirectURLMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """

    http_method_names = ["post", "options"]
    template_name = "registration/logged_out.html"
    extra_context = None

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        auth_logout(request)
        redirect_to = self.get_success_url()
        if redirect_to != request.get_full_path():
            # Redirect to target page once the session has been cleared.
            return HttpResponseRedirect(redirect_to)
        return super().get(request, *args, **kwargs)

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            return resolve_url(settings.LOGOUT_REDIRECT_URL)
        else:
            return self.request.path

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update(
            {
                "site": current_site,
                "site_name": current_site.name,
                "title": _("Logged out"),
                "subtitle": None,
                **(self.extra_context or {}),
            }
        )
        return context


def logout_then_login(request, login_url=None):
    """
    Log out the user if they are logged in. Then redirect to the login page.
    """
    login_url = resolve_url(login_url or settings.LOGIN_URL)
    return LogoutView.as_view(next_page=login_url)(request)


def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[4] = querystring.urlencode(safe="/")

    return HttpResponseRedirect(urlunparse(login_url_parts))


# Class-based password reset views
# - PasswordResetView sends the mail
# - PasswordResetDoneView shows a success message for the above
# - PasswordResetConfirmView checks the link the user clicked and
#   prompts for a new password
# - PasswordResetCompleteView shows a success message for the above


class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "registration/password_reset_form.html"
    title = _("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"


class PasswordResetDoneView(PasswordContextMixin, TemplateView):
    template_name = "/password_reset_done.html"
    title = _("Password reset sent")


class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "password_reset/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())

    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context


class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = PasswordChangeForm
    #success_url = reverse_lazy("password_change_done")
    #template_name = "registration/password_change_form.html"
    #template_name = "password_reset/password_change.html"
    title = _("Password change")

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        return super().form_valid(form)


class PasswordChangeDoneView(PasswordContextMixin, TemplateView):
    #template_name = "password_reset/password_change_done.html"
    template_name = "home.html"
    title = _("Password Change Successful")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)












