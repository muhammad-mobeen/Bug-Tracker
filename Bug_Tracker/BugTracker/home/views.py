from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import BugTickets, SortedBugTickets
from home.forms import BugTicketsForm

# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, username=username, password=password)

        if user != None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or Password does not exist!')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def index(request):
    form = BugTicketsForm()
    if request.method == "POST":
        request.POST = request.POST.copy()

        #Logic for priorit from string to int
        if request.POST.get('priority') == "Urgent":
            request.POST['priority'] = int(1)
        elif request.POST.get('priority') == "High":
            request.POST['priority'] = int(2)
        elif request.POST.get('priority') == "Medium":
            request.POST['priority'] = int(3)
        else:
            request.POST['priority'] = int(4)

        form = BugTicketsForm(request.POST)
        print(request.POST)
        if form.is_valid():
            try:
                form.save()
                # Update Sorted Tickets Database
                updateSortedBugTickets()
                return redirect("home")
            except:
                print("Not sved!!!!!")
                pass
        else:
            print("The Form is not valid! Hence not submited!")

    else:
        form = BugTicketsForm()

    return render(request, "index.html", {'form':form})

def show(request):
    updateSortedBugTickets()
    tickets = BugTickets.objects.all()
    sorted_tickets = SortedBugTickets.chandiyo.all()
    return render(request, "show.html", {'tickets': tickets, 'sorted_tickets': sorted_tickets})

def edit(request, id):
    ticket = BugTickets.objects.get(id=id)
    return render(request, "index.html", {'ticket': ticket})

def update(request, id):
    ticket = BugTickets.objects.get(id=id)
    request.POST = request.POST.copy()

    #Logic for priorit from string to int
    if request.POST.get('priority') == "Urgent":
        request.POST['priority'] = int(1)
    elif request.POST.get('priority') == "High":
        request.POST['priority'] = int(2)
    elif request.POST.get('priority') == "Medium":
        request.POST['priority'] = int(3)
    else:
        request.POST['priority'] = int(4)

    form = BugTicketsForm(request.POST, instance= ticket)
    print(request.POST)
    if form.is_valid():
        form.save()
        return redirect('show')
    return render(request, "show.html", {'ticket': ticket})

def delete(request, id):
    ticket = BugTickets.objects.get(id=id)
    ticket.delete()
    return redirect("show")

def updateSortedBugTickets():
    SortedBugTickets.chandiyo.all().delete()
    SortedBugTickets.chandiyo.testSaver()