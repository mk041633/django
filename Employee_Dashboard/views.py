from logging import exception
from django.shortcuts import render, redirect
from django.contrib import messages
from . models import Tasks
import pdb;
import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from authentication.models import User
from Employer_Dashboard.models import Department



def dashboardView(request):
    task = Tasks.objects.filter(owner=request.user)
    return render (request, 'Employee_Dashboard/dashboard_base.html', {'task':task} )

def EmployeeProfileView(request):
    dept = Department.objects.all()
    if request.method=="GET":
        user = User.objects.get(username=request.user.username)
        username = user.username
        request.session['username'] = username
        password = user.password
        number = user.id
        department = user.last_name
        email = user.email
        date = user.date_joined
        date = str(date)[:10]
        context = {
            'dept':dept, 'username':username, 'password':password, 'number':number, 'department':department, 'email':email, 'date':date
        }

        return render (request, 'Employee_Dashboard/profile.html', context)
    else:
        return render (request, 'Employee_Dashboard/profile.html', context)

def AddTaskView(request):
    maxdate = datetime.datetime.now()
    maxdate = str(maxdate)
    time = maxdate[11:16]
    maxdate = maxdate[:10]+'T'+time 
    if request.method=="GET":
        return render(request, 'Employee_Dashboard/AddTask.html', {'maxdate':maxdate})
    if request.method=="POST":
        description = request.POST['description']
        type = request.POST['type']
        Datetime = request.POST['datetime']
        time = request.POST['time']
        Date = str(Datetime)
        Date = Date[:10]
        Tasks.objects.create(owner=request.user,StartDate=Date, Description=description, Type=type, StartTime=Datetime, TimeTaken=time)
        messages.success(request, "Задача успешно добавлена")
        return redirect('nadd-task')



def GetTodayTasksView(request):
    today = datetime.date.today()
    today = str(today)
    Ttasks = Tasks.objects.filter(owner=request.user, StartDate=today)
    Tfinalrep = {}
    def Tget_type(Ttasks):
        return Ttasks.Type
    Ttask_list = list(set(map(Tget_type, Ttasks)))
    def Tget_type_time(Type):
        Ttime=0
        Tfiltered_by_type = Ttasks.filter(Type=Type)
        for item in Tfiltered_by_type:
            Ttime += item.TimeTaken
        return Ttime

    for x in Ttasks:
        for y in Ttask_list:
            Tfinalrep[y] = Tget_type_time(y)
    return JsonResponse({'Ttype_time_data': Tfinalrep}, safe=False)


def GetYestTasksView(request):
    yesterday = (datetime.date.today() - datetime.timedelta(1)).strftime('%Y-%m-%d')    
    Ytasks = Tasks.objects.filter(owner=request.user, StartDate=yesterday)
    Yfinalrep = {}
    def Yget_type(Ytasks):
        return Ytasks.Type
    Ytask_list = list(set(map(Yget_type, Ytasks)))
    def Yget_type_time(YType):
        Ytime=0
        Yfiltered_by_type = Ytasks.filter(Type=YType)
        for item in Yfiltered_by_type:
            Ytime += item.TimeTaken
        return Ytime

    for x in Ytasks:
        for y in Ytask_list:
            Yfinalrep[y] = Yget_type_time(y)
    return JsonResponse({'Ytype_time_data': Yfinalrep}, safe=False)

def GetWeeklyTasksView(request):
    today = datetime.datetime.now()
    monday = str(today - datetime.timedelta(today.weekday()))[:10]
    tuesday = str(today - datetime.timedelta(today.weekday()-1))[:10]
    wednesday = str(today - datetime.timedelta(today.weekday()-2))[:10]
    thursday = str(today - datetime.timedelta(today.weekday()-3))[:10]
    friday = str(today - datetime.timedelta(today.weekday()-4))[:10]
    saturday = str(today - datetime.timedelta(today.weekday()-5))[:10]
    sunday = str(today + datetime.timedelta(7-today.weekday()-1))[:10]
    Wtasks = Tasks.objects.filter(owner=request.user)
    Wfinalrep = {}
    def Wget_type(Wtasks):
        return Wtasks.Type
    Wtask_list = list(set(map(Wget_type, Wtasks)))
    monbreakc=0
    monworkc=0
    monmeetc=0
    monbreak = Tasks.objects.filter(owner=request.user, StartDate=monday,Type='Перерыв')
    monwork = Tasks.objects.filter(owner=request.user, StartDate=monday,Type='Работа')
    monmeet = Tasks.objects.filter(owner=request.user, StartDate=monday,Type='Встреча')
    for i in monbreak:
        monbreakc = monbreakc+i.TimeTaken
    for i in monwork:
        monworkc = monworkc+i.TimeTaken
    for i in monmeet:
        monmeetc=monmeetc+i.TimeTaken
    tuebreakc=0
    tueworkc=0
    tuemeetc=0
    tuebreak = Tasks.objects.filter(owner=request.user, StartDate=tuesday,Type='Перерыв')
    tuework = Tasks.objects.filter(owner=request.user, StartDate=tuesday,Type='Работа')
    tuemeet = Tasks.objects.filter(owner=request.user, StartDate=tuesday,Type='Встреча')
    for i in tuebreak:
        tuebreakc = tuebreakc+i.TimeTaken
    for i in tuework:
        tueworkc = tueworkc+i.TimeTaken
    for i in tuemeet:
        tuemeetc=tuemeetc+i.TimeTaken
    wedbreakc=0
    wedworkc=0
    wedmeetc=0
    wedbreak = Tasks.objects.filter(owner=request.user, StartDate=wednesday,Type='Перерыв')
    wedwork = Tasks.objects.filter(owner=request.user, StartDate=wednesday,Type='Работа')
    wedmeet = Tasks.objects.filter(owner=request.user, StartDate=wednesday,Type='Встреча')
    for i in wedbreak:
        wedbreakc = wedbreakc+i.TimeTaken
    for i in wedwork:
        wedworkc = wedworkc+i.TimeTaken
    for i in wedmeet:
        wedmeetc=wedmeetc+i.TimeTaken
    thubreakc=0
    thuworkc=0
    thumeetc=0
    thubreak = Tasks.objects.filter(owner=request.user, StartDate=thursday,Type='Перерыв')
    thuwork = Tasks.objects.filter(owner=request.user, StartDate=thursday,Type='Работа')
    thumeet = Tasks.objects.filter(owner=request.user, StartDate=thursday,Type='Встреча')
    for i in thubreak:
        thubreakc = thubreakc+i.TimeTaken
    for i in thuwork:
        thuworkc = thuworkc+i.TimeTaken
    for i in thumeet:
        thumeetc=thumeetc+i.TimeTaken
    fribreakc=0
    friworkc=0
    frimeetc=0
    fribreak = Tasks.objects.filter(owner=request.user, StartDate=friday,Type='Перерыв')
    friwork = Tasks.objects.filter(owner=request.user, StartDate=friday,Type='Работа')
    frimeet = Tasks.objects.filter(owner=request.user, StartDate=friday,Type='Встреча')
    for i in fribreak:
        fribreakc = fribreakc+i.TimeTaken
    for i in friwork:
        friworkc = friworkc+i.TimeTaken
    for i in frimeet:
        frimeetc=frimeetc+i.TimeTaken
    satbreakc=0
    satworkc=0
    satmeetc=0
    satbreak = Tasks.objects.filter(owner=request.user, StartDate=saturday,Type='Перерыв')
    satwork = Tasks.objects.filter(owner=request.user, StartDate=saturday,Type='Работа')
    satmeet = Tasks.objects.filter(owner=request.user, StartDate=saturday,Type='Встреча')
    for i in satbreak:
        satbreakc = satbreakc+i.TimeTaken
    for i in satwork:
        satworkc = satworkc+i.TimeTaken
    for i in satmeet:
        satmeetc=satmeetc+i.TimeTaken
    sunbreakc=0
    sunworkc=0
    sunmeetc=0
    sunbreak = Tasks.objects.filter(owner=request.user, StartDate=sunday,Type='Перерыв')
    sunwork = Tasks.objects.filter(owner=request.user, StartDate=sunday,Type='Работа')
    sunmeet = Tasks.objects.filter(owner=request.user, StartDate=sunday,Type='Встреча')
    for i in sunbreak:
        sunbreakc = sunbreakc+i.TimeTaken
    for i in sunwork:
        sunworkc = sunworkc+i.TimeTaken
    for i in sunmeet:
        sunmeetc=sunmeetc+i.TimeTaken
    MONDAY = {'monbreakc':monbreakc,'monworkc': monworkc,'monmeetc':monmeetc}
    TUESDAY = {'tuebreakc': tuebreakc,'tueworkc':tueworkc,'tuemeetc':tuemeetc}
    WEDNESDAY = {'wedbreakc':wedbreakc,'wedworkc':wedworkc,'wedmeetc':wedmeetc}
    THURSDAY = {'thubreakc':thubreakc,'thuworkc':thuworkc,'thumeetc':thumeetc}
    FRIDAY = {'fribreakc':fribreakc,'friworkc':friworkc,'frimeetc':frimeetc}
    SATURDAY = {'satbreakc':satbreakc,'satworkc':satworkc,'satmeetc':satmeetc}
    SUNDAY = {'sunbreakc':sunbreakc,'sunworkc':sunworkc,'sunmeetc':sunmeetc}
    return JsonResponse({'MONDAY': MONDAY, 'TUESDAY':TUESDAY,'WEDNESDAY':WEDNESDAY,'THURSDAY':THURSDAY,'FRIDAY':FRIDAY,'SATURDAY':SATURDAY,'SUNDAY':SUNDAY}, safe=False)


cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='/authentication/login')
def DateFilterView(request):
    if request.method =='GET':
        return redirect('ndashboard')
    if request.method=='POST':
        date = request.session['date']
        Ftasks = Tasks.objects.filter(owner=request.user, StartDate=date)
        Ffinalrep = {}
        def Fget_type(Ftasks):
            return Ftasks.Type
        Ftask_list = list(set(map(Fget_type, Ftasks)))
        def Fget_type_time(FType):
            Ftime=0
            Ffiltered_by_type = Ftasks.filter(Type=FType)
            for item in Ffiltered_by_type:
                Ftime += item.TimeTaken
            return Ftime

        for x in Ftasks:
            for y in Ftask_list:
                Ffinalrep[y] = Fget_type_time(y)
        return JsonResponse({'Ftype_time_data': Ffinalrep}, safe=False)

def CallDateFilterView(request):
    maxdate = datetime.datetime.now()
    maxdate = str(maxdate)
    maxdate = maxdate[:10]
    if request.method=="GET":
        return render(request, 'Employee_Dashboard/ViewSymmaryDate.html',{'maxdate':maxdate})
    else:
        date = request.POST['date']
        request.session['date'] = date
        return render(request, 'Employee_Dashboard/Final.html',{'maxdate':maxdate})