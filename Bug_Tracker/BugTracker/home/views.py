from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import BugTickets

# Create your views here.
def index(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        #Logic for priorit from string to int
        if request.POST.get('priority') == "Urgent":
            priority = 1
        elif request.POST.get('priority') == "High":
            priority = 2
        elif request.POST.get('priority') == "Medium":
            priority = 3
        else:
            priority = 4
        
        index = BugTickets(title=title, description=description, priority=priority, date=datetime.today())
        index.save()

    return render(request, 'index.html')