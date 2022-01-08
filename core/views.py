from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .helpers import prediction

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def plag_check(request):
    return render(request, 'output.html')

def dev_page(request):
    if request.method == "POST":
        file = request.FILES['pdfUpload']
        query = request.POST['query']
        fs = FileSystemStorage(location="media/pdfUploads/")
        fs.save(file.name, file)
        
        r, urls= prediction(file.name, query, searchlevel=20)
        print(r)
        print(urls)
        
        return redirect('home-page')
    return render(request, 'dev.html')

