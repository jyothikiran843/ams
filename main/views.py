from datetime import date, datetime,time,timedelta
from time import strftime
from django.http import HttpResponse
from django.shortcuts import render,redirect
import sqlite3

response=HttpResponse()
# Create your views here.
def index(request):
    if request.COOKIES.get('id',None):
        return redirect('main/')
    else:
        return render(request,'index.html')

def main(request):
    if request.method=='POST':
        if request.COOKIES.get('id',None):
            return HttpResponse("Hi "+request.COOKIES['id'].upper())
        else:
           connect()
           cursor.execute("SELECT class FROM details WHERE id='"+request.POST['idnum']+"';")
           c=cursor.fetchall()
           if c:
            section=c[0][0]
            response=redirect('/')
            response.set_cookie('id',value=request.POST.get('idnum'))
            response.set_cookie('class',value=section)
            return response
           else:
            return render(request,'error.html',{'flag':'branch'})
    else:  
        if request.COOKIES.get('id',None):
            ds={'1':'m','2':'tu','3':'w','4':'th','5':'f','6':'s'}
            # duration=timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=30, hours=1, weeks=0)
            now=datetime.now()
            day=now.strftime('%w')
            # day='6'
            hr=now.hour
            # hr=15
            min=now.minute
            if min<10:
                min=str("0"+str(min))
            elif min==0:
                min='00'
            t=int(str(hr)+str(min))
            print(t)
            if t>=915 and t<1015:
                current_slot="1"
            elif t>=1015 and t<1115:
                current_slot="2"
            elif t>=1115 and t<1215:
                current_slot="3"
            elif t>=1215 and t<1315:
                current_slot="4"
            elif t>=1415 and t<1715:
                current_slot="5"
            else:
                current_slot="0"
            print(current_slot)
            connect()
            cursor.execute("SELECT id,name,class FROM details WHERE id='"+request.COOKIES['id']+"';")
            global student
            student=cursor.fetchall()[0]
            if day=='0':
                return render(request,'main.html',{'flag':'holiday','id':student[0],'name':student[1],'class':student[2],'date':now})
            else:
                if check_table(request):
                    cursor.execute("SELECT * FROM "+request.COOKIES['class']+" WHERE week='"+ds[day]+"';")
                    classes=cursor.fetchall()
                    if not classes:
                        return render(request,'main.html',{'flag':'no-slot','id':student[0],'name':student[1],'class':student[2],'date':now})
                    elif classes:
                        print(classes)
                        classes=classes[0]
                        subs=['cn','se','os','mfds','dm','selab','cnlab','englab','oslab']
                        slots_list=list(classes[1:])
                        slots=dict(zip(subs,slots_list))
                        print(len(subs),len(classes[1:]),subs,slots_list)
                        print(slots)
                        if current_slot=='0':
                            return render(request,'main.html',{'flag':'no-slot','id':student[0],'name':student[1],'class':student[2],'date':now})
                        for i in slots.keys():
                            if slots[i]==current_slot:
                                print(i)
                                return render(request,'main.html',{'flag':i,'id':student[0],'name':student[1],'class':student[2],'date':now})
                        return render(request,'main.html',{'flag':'no-slot','id':student[0],'name':student[1],'class':student[2],'date':now})
                    else:
                        return render(request,'error.html',{'flag':'timetable','id':student[0],'name':student[1],'class':student[2],'date':now})
                else:
                    create_table(request)
                    print("Table for "+request.COOKIES['class']+" is created")
                    return render(request,'error.html',{'flag':'timetable','id':student[0],'name':student[1],'class':student[2],'date':now})
        else:
            return redirect('/')

def set_schedule(request):
    if request.COOKIES.get('id',None):
        if request.COOKIES['id']=='N180333':   
            if request.method=='POST':
                if check_table(request):
                    cursor.execute("DELETE FROM "+request.COOKIES['class']+";")
                    conn.commit()
                    insert_data(request)
                    print('table updates')
                else:
                    create_table(request)
                    insert_data(request)
                    print("data inserted")
                print(request.POST)
                return render(request,'schedules.html',{'flag':True})
            else:
                return render(request,'schedules.html')
        else:
            response=HttpResponse("This page can be accessed by CR and Admin only")
            response=redirect('/')
            return response
    else:
        return redirect('/')
def show_all(request):
    if request.COOKIES.get('class',None):
        connect()
        cursor.execute("SELECT * FROM "+request.COOKIES['class']+";")
        print("SELECT * FROM "+request.COOKIES['class']+";")
        print("Heree are details")
        print(cursor.fetchall())
        return HttpResponse("Check in cline")
    else:
        return HttpResponse("Device not Mapped")
def attend(request):
    if request.method=='POST':
        subject=request.POST.get('Attend')
        now=datetime.now()
        now=str("date"+now.strftime("%d%m%y"))
        print(now)
        connect()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables=cursor.fetchall()
        if (subject,) in tables:
            cols=cursor.execute("SELECT * FROM "+subject+";")
            dates=[]
            for i in cols.description:
                dates.append(i[0])
            print("date olumn:",dates)
            if now in dates:
                return attended(request,subject,now)
            else:
                cursor.execute("ALTER TABLE "+subject+" ADD COLUMN "+now+" varchar(20);")
                conn.commit()
                return attended(request,subject,now)
        else:
            cursor.execute("CREATE TABLE "+subject+"(id,class,"+now+");")
            conn.commit()
            return attended(request,subject,now)
    else:
        return HttpResponse("Bad Gateway")
def query(request):
    if request.method=='POST':
        if (request.POST.get('uname')=='jyothikiran') and (request.POST.get('pwd')=='root'):
            return render(request,'query.html',{'flag':True})
        else:
            return HttpResponse("Authentication Failed Please Try Again")
    else:
        return render(request,'query.html',{'flag':False})
def execute_query(request):
    if request.method=='POST':
        if request.POST.get('query')=='Commit':
            connect()
            cursor.execute(request.POST['query_string'])
            print(cursor.fetchall())
            conn.commit()
            if(cursor):
                return HttpResponse("Success")
            else:
                return HttpResponse("Something's not right")
        else:
            return HttpResponse("Not a Correct a way")
    else:
        return HttpResponse("Bad Gateway")
def create_table(request):
    global cursor,conn
    cursor.execute("CREATE TABLE "+request.COOKIES['class']+"(week varchar(10) NOT NULL PRIMARY KEY,cn varchar(1),se varchar(1),os varchar(1),mfds varchar(1),dm varchar(1),selab varchar(1),cnlab varchar(1),englab varchar(1),oslab varchar(1));")
    conn.commit()
def insert_data(request):
    global cursor,conn
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('m',"+request.POST.get('mcnslot')+","+request.POST.get('mseslot')+","+request.POST.get('mosslot')+","+request.POST.get('mmfdsslot')+","+request.POST.get('mdmslot')+","+request.POST.get('mselslot')+","+request.POST.get('mcnlslot')+","+request.POST.get('melslot')+","+request.POST.get('moslslot')+");"
    cursor.execute(query)
    conn.commit()
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('tu',"+request.POST.get('tucnslot')+","+request.POST.get('tuseslot')+","+request.POST.get('tuosslot')+","+request.POST.get('tumfdsslot')+","+request.POST.get('tudmslot')+","+request.POST.get('tuselslot')+","+request.POST.get('tucnlslot')+","+request.POST.get('tuelslot')+","+request.POST.get('tuoslslot')+");"
    cursor.execute(query)
    conn.commit()
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('w',"+request.POST.get('wcnslot')+","+request.POST.get('wseslot')+","+request.POST.get('wosslot')+","+request.POST.get('wmfdsslot')+","+request.POST.get('wdmslot')+","+request.POST.get('wselslot')+","+request.POST.get('wcnlslot')+","+request.POST.get('welslot')+","+request.POST.get('woslslot')+");"
    cursor.execute(query)
    conn.commit()
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('th',"+request.POST.get('thcnslot')+","+request.POST.get('thseslot')+","+request.POST.get('thosslot')+","+request.POST.get('thmfdsslot')+","+request.POST.get('thdmslot')+","+request.POST.get('thselslot')+","+request.POST.get('thcnlslot')+","+request.POST.get('thelslot')+","+request.POST.get('thoslslot')+");"
    cursor.execute(query)
    conn.commit()
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('f',"+request.POST.get('fcnslot')+","+request.POST.get('fseslot')+","+request.POST.get('fosslot')+","+request.POST.get('fmfdsslot')+","+request.POST.get('fdmslot')+","+request.POST.get('fselslot')+","+request.POST.get('fcnlslot')+","+request.POST.get('felslot')+","+request.POST.get('foslslot')+");"
    cursor.execute(query)
    conn.commit()
    query="INSERT INTO "+request.COOKIES['class']+" VALUES('s',"+request.POST.get('scnslot')+","+request.POST.get('sseslot')+","+request.POST.get('sosslot')+","+request.POST.get('smfdsslot')+","+request.POST.get('sdmslot')+","+request.POST.get('sselslot')+","+request.POST.get('scnlslot')+","+request.POST.get('selslot')+","+request.POST.get('soslslot')+");"
    cursor.execute(query)
    conn.commit()
def connect():
    global conn,cursor
    conn=sqlite3.connect('db.sqlite3')
    cursor=conn.cursor()
def check_table(request):
    connect()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables=cursor.fetchall()
    print(tables)
    if (request.COOKIES['class'],) in tables:
        print("Exists")
        return True
    else:
        print("not exists")
        return False
def attended(request,subject,now):
    # connect()
    cursor.execute("SELECT "+now+" FROM "+subject+" WHERE id='"+request.COOKIES['id']+"';")
    a=cursor.fetchall()
    print(a)
    if a:
        print(a)
        if a[0]==('1',):
            print(a)
            return render(request,'main.html',{'flag':'already','sub':subject,'name':student[1],'id':student[0],'class':student[2]})
    cursor.execute("INSERT INTO "+subject+"(id,class,"+now+") VALUES('"+request.COOKIES['id']+"','"+request.COOKIES['class']+"','"+'1'+"');")
    conn.commit()
    return render(request,'main.html',{'flag':'attended','sub':subject,'name':student[1],'id':student[0],'class':student[2],'date':now})
print(datetime.now())