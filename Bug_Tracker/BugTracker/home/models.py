from django.db import models

# Create your models here.

class BugTickets(models.Model):
    title = models.CharField(max_length=122,)
    description = models.TextField()
    priority = models.IntegerField()
    date = models.DateField()