from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .forms import info,leaveinfo
from .models import Details,Leave
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
import calendar


# def Sick_leave(username):
#     sum=0
#     val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Sick Leave')
#     for x in val:
#         sum=sum+ x.totaldays    
#     slv=sum
#     return slv


@login_required
def leave_req(request,username):
    # casual leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Casual Leave')
    for x in val:
        sum=sum+x.totaldays    
    clv=sum

    # sick leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Sick Leave')
    for x in val:
        sum=sum+ x.totaldays    
    slv=sum
    # Sick_leave(username)

    # vaccation leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Vacation Leave')
    for x in val:
        sum=sum+x.totaldays    
    vlv=sum

    
# medical leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Medical Leave')
    for x in val:
        sum=sum+x.totaldays    
    mlv=sum
    
    if request.method=="POST":
        # form=leaveinfo(request.POST)
        user_name=request.POST['username']
        e_mail=request.POST['email']
        leave_type=request.POST['leavetype']
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        total_days=request.POST['totaldays']
        rea_son=request.POST['reason']
        req_status=request.POST['reqstatus']
        # this method has to be followed for inserting data into the table
        form=Leave.objects.create(username=username,email=e_mail,leavetype=leave_type,startdate=start_date,enddate=end_date,totaldays=total_days,reason=rea_son,reqstatus=req_status)

        info = Details.objects.all().filter(username=username)
        return render(request,'app/customer.html',{'info': info})
    else:
        form=Details.objects.get(username=username)
        return render(request,'app/leave_req.html',{'form':form,'slv':slv,'mlv':mlv,"vlv":vlv,'clv':clv})
    

def leave_search(request,username):
    if request.method == 'POST':
        start_date=request.POST['start-date']
        end_date=request.POST['end-date']
        data=Leave.objects.all().filter(username=username,startdate__range=[start_date, end_date],reqstatus='accept')
        # data=Leave.objects.raw ('SELECT (leavetype,startdate,enddate,totaldays,reason) FROM Leave WHERE startdate BETWEEN "'+ start_date + '" AND "' + end_date + '"')
        # data=Leave.objects.raw('select (leavetype,startdate,enddate,totaldays,reason) from Leave where startdate between '+ start_date + 'and' + end_date + '')
        return render(request,'app/leave_search.html',{'data':data})
    else:
        return render(request,'app/leave_search.html')


@login_required
def pending(request):
    data=Leave.objects.filter(reqstatus="pending")
    return render(request,'app/pending.html',{'data':data})


@login_required
def accepted(request):
    data=Leave.objects.filter(reqstatus="accept")
    return render(request,'app/accept.html',{'data':data})


@login_required
def rejected(request):
    data=Leave.objects.filter(reqstatus="reject")
    return render(request,'app/reject.html',{'data':data})


@login_required
def accept(request,id):
    data=Leave.objects.get(id=id)   
    data.reqstatus="accept"
    data.save()
    return redirect('pending')


@login_required
def reject(request,id):
    data=Leave.objects.get(id=id)   
    data.reqstatus="reject"
    data.save()
    return redirect('pending')


@login_required
def user_summary(request,username):
    # month
    val = datetime.now().month
    month=calendar.month_name[val]
    #########################

    asl=5
    aml=10
    avl=10
    acl=1
    

# sick leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Sick Leave')
    for x in val:
        sum=sum+ x.totaldays    
    sl=sum
    bsl=5-sl

    
# casual leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Casual Leave')
    for x in val:
        sum=sum+x.totaldays    
    cl=sum
    bcl=1-cl

# vaccation leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Vacation Leave')
    for x in val:
        sum=sum+x.totaldays    
    vl=sum
    bvl=10-vl

    
# medical leave
    sum=0
    val=Leave.objects.all().filter(username=username,reqstatus='accept',leavetype='Medical Leave')
    for x in val:
        sum=sum+x.totaldays    
    ml=sum
    bml=10-ml


# total
    ttl=acl+asl+aml+avl
    t_tkn=sl+ml+vl+cl
    t_bal=26-t_tkn
# yearly
    tl=35
    bal=tl-t_tkn

    if request.method == 'POST':
        start_date=request.POST['start-date']
        end_date=request.POST['end-date']
        data=Details.objects.get(username=username)
        value=Leave.objects.all().filter(username=username,startdate__range=[start_date, end_date],reqstatus='accept')
        output={'data':data,'tl':tl,'ttl':ttl,'aml':aml,'acl':acl,'avl':avl,'asl':asl,'value':value,'month':month,'bal':bal,'sl':sl,'cl':cl,'vl':vl,'ml':ml,'t_tkn':t_tkn,'t_bal':t_bal,'bsl':bsl,'bml':bml,'bcl':bcl,'bvl':bvl}
        return render(request,'app/user_summary.html',output)
    else:
        value=Leave.objects.all().filter(username=username)
        data=Details.objects.get(username=username)
        output={'data':data,'tl':tl,'ttl':ttl,'aml':aml,'acl':acl,'avl':avl,'asl':asl,'value':value,'month':month,'bal':bal,'sl':sl,'cl':cl,'vl':vl,'ml':ml,'t_tkn':t_tkn,'t_bal':t_bal,'bsl':bsl,'bml':bml,'bcl':bcl,'bvl':bvl}
        return render(request,'app/user_summary.html',output)

    





def home(request):
    return render(request,'app/home.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user =authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
        # if user.is_superuser:
            login(request, user)
            return redirect('employee',permanent=False)

        elif user is not None and user.is_staff:
            login(request, user)
            info = Details.objects.all().filter(username=username)
            # return redirect('customer',permanent=False)
            return render(request,'app/customer.html',{'info': info})

        else:
            # messages.info(request, 'Invalid Credentials')
            return redirect('signin')
    return render(request,'app/signin.html')

def signout(request):
    logout(request)
    return redirect('home')

@login_required
def register(request):
    if request.method == "POST":
        form=info(request.POST)
        if form.is_valid:
            form.save()
            username = request.POST['username']
            name = request.POST['name']
            email = request.POST['email']
            status = request.POST['status']
            password = request.POST['password']
            
            user = User.objects.create_user(username, email, password)
            user.first_name = name
            if status=="employee":
                user.is_superuser=True
                user.is_staff=True
                user.is_active=True
            elif status=="customer":
                user.is_superuser=False
                user.is_staff=True
                user.is_active=True
            else:
                pass
            user.save()
            return redirect("home")    
        else:
            # form=info()
            return render(request,'app/register.html',{'form':form})
    else:
        return render(request,'app/register.html')


@login_required
def employee(request):
    data=Details.objects.all()
    # value=User.objects.all()
    return render(request,'app/employee.html',{'data':data})

@login_required
def active_users(request):
    value=User.objects.all()
    return render(request,'app/active_users.html',{'value':value})

@login_required
def customer(request,username):
    info=Details.objects.get(username=username)
    return render(request,'app/customer.html',{'info': info})

@login_required
def admin_update(request,username):
    val= Details.objects.get(username=username)
    edit= User.objects.get(username=username)
    # val=Details.objects.get(id=id)
    # edit=User.objects.get(id=id)

    if request.method=='POST':
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        status = request.POST['status']
        # password = request.POST['password']
        # repassword = request.POST['repassword']

        val.username=username
        edit.username=username
        val.name=name
        edit.first_name=name
        val.email=email
        edit.email=email
        if status=="active":
            edit.is_active=True
        else:
            edit.is_active=False
        # val.password=password
        # edit.password=password
        # val.repassword=repassword
        val.save()
        edit.save()
        return redirect("employee")
    else:
        return render (request,"app/admin_update.html",{'val':val})


# deletes the data in the db and not in the usertable and makes it inactive
@login_required
def admin_delete(request,username):
    delt= Details.objects.get(username=username)
    trash= User.objects.get(username=username)
    delt.delete()
    trash.is_active=False
    trash.save()
    return redirect("employee")


# @login_required
def paswd_change(request,username):
    pas=User.objects.get(username=username)
    val=Details.objects.get(username=username)

    if request.method == 'POST':
        old = request.POST['old']
        old_pass=pas.password
        new = request.POST['new']
        confirm = request.POST['confirm']
        # print(old_pass)
        if old != old_pass:
            if confirm == new:
                pas.set_password(new)
                val.password=new
                val.repassword=new
                val.save()
                pas.save()
                # update_session_auth_hash(request,pas.User)
            # messages.info(request, "Password changed successfully")
                return redirect('home')
            else:
                # messages.success(request, "New password and confirm password are not same.")
                return HttpResponse('Invalid Credentials')
        else:
            return HttpResponse('wrong old password')
    else:
        return render(request,'app/paswd_change.html')








