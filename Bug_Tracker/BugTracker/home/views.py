from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    context = {
        "var":"Wah Yar thi bhi agya krna you sneaky boi@@!!!"
    }
    return render(request, 'index.html', context)