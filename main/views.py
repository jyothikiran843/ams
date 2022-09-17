from wsgiref.util import request_uri
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
           response=redirect('/')
           response.set_cookie('id',value=request.POST.get('idnum'))
           response.set_cookie('class',value=request.POST.get('class'))
           return response
    else:  
        if request.COOKIES.get('id',None):
            if request.COOKIES.get('class',None):
                return render(request,'main.html',{'class':request.COOKIES['class'],'id':request.COOKIES['id']})
            else:
                return HttpResponse("Please contact admin")
        else:
            return redirect('/')

def set_schedule(request):
    if request.COOKIES.get('id',None):
        if request.COOKIES['id']=='N180333':   
            if request.method=='POST':
                conn=sqlite3.connect('db.sqlite3')
                cursor=conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                tables=cursor.fetchall()
                print("tables are: ",tables)
                if (request.COOKIES['class'],) in tables:
                    cursor.execute("DELETE FROM "+request.COOKIES['class']+";")
                    conn.commit()
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
                    print('table updates')
                else:
                    cursor.execute("CREATE TABLE "+request.COOKIES['class']+"(week varchar(10),cn varchar(1),se varchar(1),os varchar(1),mfds varchar(1),dm varchar(1),selab varchar(1),mfdslab varchar(1),englab varchar(1),oslab varchar(1));")
                    conn.commit()
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
    conn=sqlite3.connect('db.sqlite3')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM "+request.COOKIES['class']+";")
    print("Heree are details")
    print(cursor.fetchall())
    return HttpResponse("Check in cline")