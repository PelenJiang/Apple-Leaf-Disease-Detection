from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .models import *
import os
#main
def index_views(request):
    return render(request, 'index.html')

def upload_image(request,shell=True):
	obj = request.FILES.get('inputfile')
	filename=obj.name
	print(filename)
	file_path = os.path.join("static/upload", filename)
	f = open(file_path, 'wb')
	for chunk in obj.chunks():
		f.write(chunk)
	f.close()
	print(file_path)
	File.objects.create(file_name=filename,file_size=obj.size,file=file_path)
	return HttpResponseRedirect('/show')   
def show_image(request):
    files=File.objects.all().order_by('create_time').last()
    return render(request,'show.html',locals())

def dete1(request):
	import detection
	files=File.objects.all().order_by('create_time').last()
	detection.runjpg1(files.file)
	return HttpResponseRedirect('/result')
def result(request):
	return render(request,'result.html')
def about_views(request):
	return render(request,'about.html')
def project_views(request):
	return render(request,'projects.html')
def contact_views(request):
	return render(request,'contact.html')
def suggest_views(request):
	return render(request,'suggest.html')