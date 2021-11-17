from django.shortcuts import render
from index import util
from index import form
from PIL import Image
num_images=0
def index(request):
    return render(request, 'index.html',locals())
def about(request):
    return render(request, 'about.html',locals())
def contact(request):
    return render(request, 'contact.html',locals())
def projects(request):
    return render(request, 'projects.html',locals())
def result(request):
    return render(request, 'result.html',locals())
def show(request):
    return render(request, 'show.html',locals())
def singlepost(request):
    return render(request, 'singlepost.html',locals())
def suggest(request):
    return render(request, 'suggest.html',locals())
def upload(request):
    global num_images
    imagename='statics/results_images/%s.jpg'%num_images
    num_images+=1
    form2 = form.FilesForm(request.POST or None, request.FILES or None)
    if form2.is_valid():
        image = form2.cleaned_data['image']
        image=Image.open(image)
        image=util.recognition(image)
        image.save(imagename)
    print ("我想输出的是："+str(image))
    return render(request, 'result.html',locals())
# Create your views here.
