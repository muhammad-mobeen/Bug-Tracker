from django.forms import ModelForm, Textarea
from django.db import models
from home.logic import LinkedList, MergeSort
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)

    avatar = models.ImageField(null=True, default="markhor.jpg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class BugTickets(models.Model):
    title = models.CharField(max_length=122,)
    description = models.TextField(max_length=500, null=True, blank=True)
    priority = models.IntegerField()
    assigned_to = models.ManyToManyField(User, related_name='assigned_to', blank=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=122, default="unopened")
    update_date = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "bug_tickets"

class SortedBugTicketsManager(models.Manager):
    def testSaver(self):
        tickets = BugTickets.objects.all()
        saver = None
        llist = LinkedList()
        for ticket in tickets.iterator():
            llist.append(ticket.id, ticket.priority)
        MergeSort(llist)

        #From Sorted LinkedList to Database
        if llist.head:
            temp = llist.head
            while True:
                if temp.next == None:
                    saver = SortedBugTickets(bug_ref=temp.id, bug_priority=temp.priority)
                    saver.save()
                    break
                else:
                    saver = SortedBugTickets(bug_ref=temp.id, bug_priority=temp.priority)
                    saver.save()
                    temp = temp.next
            
        print("Saved in Sorted Database Successfully!!!")
            

class SortedBugTickets(models.Model):
    bug_ref = models.IntegerField()
    bug_priority = models.IntegerField()
    #Manager Definition
    chandiyo = SortedBugTicketsManager()

    class Meta:
        db_table = "sorted_bug_Tickets"