from multiprocessing import context
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from home.models import BugTickets, SortedBugTickets, User
from home.forms import BugTicketsForm

# Create your views here.

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')
            
        user = authenticate(request, email=email, password=password)

        if user != None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Email or Password does not exist!')
    context = {}
    return render(request, 'login.html', context)

def logoutUser(request):
    request.user.is_online = False
    request.user.save()
    logout(request)
    return redirect('dashboard')

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

@login_required(login_url='login')
def dashboard(request):
    updateSortedBugTickets()

    loged_user = request.user
    loged_user.is_online = True
    loged_user.save()

    tickets_all = BugTickets.objects.all()
    inprogress_tickets = BugTickets.objects.filter(status='inprogress')
    unopened_tickets = BugTickets.objects.filter(status='unopened')
    closed_tickets = BugTickets.objects.exclude(status='inprogress').exclude(status='unopened')
    sorted_tickets = SortedBugTickets.chandiyo.all()
    context = {
        'tickets_all': tickets_all,
        'inprogress_tickets': inprogress_tickets,
        'unopened_tickets': unopened_tickets,
        'closed_tickets': closed_tickets,
        'sorted_tickets': sorted_tickets,
        'loged_user': loged_user,
    }
    return render(request, "dashboard.html", context)

@login_required(login_url='login')
def teams(request):
    users = User.objects.all()
    tickets = BugTickets.objects.all()
    loged_user = request.user
    is_teams = True
    for user in users:
        user.reported_tickets = BugTickets.objects.filter(reported_by=user).count()
        user.assigned_tickets = BugTickets.objects.filter(assigned_to=user).filter(status='inprogress').count()
        user.completed_tickets = BugTickets.objects.filter(assigned_to=user).exclude(status='inprogress').exclude(status='unopened').count()
        try:
            user.save()
        except:
            print('some error popped!')
            pass

    context = {
        'users': users,
        'loged_user': loged_user,
        'is_teams': is_teams,
    }
    return render(request, "teams.html", context)

@login_required(login_url='login')
def add_ticket(request):
    users = User.objects.all()
    loged_user = request.user
    if request.method == "POST":
        new_ticket = BugTickets(title= request.POST.get('title'),
                                description= request.POST.get('description'),
                                priority= request.POST.get('priority'),
                                reported_by= request.user
        )
        new_ticket.save()
        for assignee in request.POST.getlist('assigned_to'):
            user = User.objects.get(username=assignee)
            new_ticket.assigned_to.add(user)
        messages.success(request, "Bug Ticket #{} ".format(new_ticket.id), extra_tags='add')
        
    context = {
        'users': users,
        'loged_user': loged_user,
    }
    return render(request, "add_ticket.html", context)

@login_required(login_url='login')
def update_status(request, id, is_completed):
    ticket = BugTickets.objects.get(id=id)
    if ticket.status == 'inprogress':
        if is_completed == 1:
            ticket.status = 'completed'
        else:
            ticket.status = 'closed'
    else:
        ticket.status = 'inprogress'
    ticket.save()
    messages.success(request, "Bug #{}: ".format(id), extra_tags='status')
    return redirect('dashboard')

@login_required(login_url='login')
def delete_ticket(request, id):
    ticket = BugTickets.objects.get(id=id)
    ticket.delete()
    messages.success(request, "Bug #{} was deleted successfully!".format(id), extra_tags='delete')
    return redirect("dashboard")

@login_required(login_url='login')
def edit_ticket(request, id):
    users = User.objects.all()
    ediTicket = BugTickets.objects.get(id=id)
    context = {
        'users' : users,
        'ediTicket': ediTicket,
    }
    return render(request, "add_ticket.html", context)

@login_required(login_url='login')
def update_ticket(request, id):
    updateTicket = BugTickets.objects.get(id=id)
    updateTicket.title = request.POST.get('title')
    updateTicket.description = request.POST.get('description')
    updateTicket.priority = request.POST.get('priority')

    updateTicket.assigned_to.clear()
    for assignee in request.POST.getlist('assigned_to'):
        user = User.objects.get(username=assignee)
        updateTicket.assigned_to.add(user)
    
    updateTicket.save()
    messages.success(request, "Bug #{}: ".format(id), extra_tags='update')
    return redirect("dashboard")

@login_required(login_url='login')
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

def updateSortedBugTickets():
    SortedBugTickets.chandiyo.all().delete()
    SortedBugTickets.chandiyo.testSaver()
