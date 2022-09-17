from django.http import HttpResponse
from django.shortcuts import render,redirect

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
            return HttpResponse("Hi "+request.COOKIES['id'])
        else:
           response=redirect('/')
           response.set_cookie('id',value=request.POST.get('idnum'))
           return response
    else:  
        if request.COOKIES.get('id',None):
            return HttpResponse("Hi "+request.COOKIES['id'])
        else:
            return redirect('/')
