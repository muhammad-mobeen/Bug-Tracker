from django.contrib import admin

from home.models import BugTickets, SortedBugTickets, User

# Register your models here.
admin.site.register(User)
admin.site.register(BugTickets)
admin.site.register(SortedBugTickets)