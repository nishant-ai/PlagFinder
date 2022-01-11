from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

from .helpers import prediction, cleanWorkingTree

# Create your views here.
def home_page(request):
    return render(request, 'index.html')

def plag_check(request):
    return render(request, 'output.html')

def dev_page(request):
    context = {}
    if request.method == "POST":
        file = request.FILES['pdfUpload']
        query = request.POST['query']
        no_of_websites = int(request.POST['no_of_websites'])
        fs = FileSystemStorage(location="media/pdfUploads/")
        fs.save(file.name, file)
        
        plag, urls= prediction(file.name, query, searchlevel=no_of_websites)
        print(plag)
        print(urls)
        context = {
            'suspected_websites' : urls,
            'plag' : plag
        }
        
        return render(request, 'plag.html', context=context)
    return render(request, 'plag.html', context=context)

