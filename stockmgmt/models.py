from django.db import models
from simple_history.models import HistoricalRecords
from django.forms import CharField
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

# Create your models here.

class Member (models.Model):
    user= models.ForeignKey (User, on_delete=models.CASCADE)
    name= models.CharField(max_length=200)

class Category (models.Model):
    name = models.CharField (max_length=50, null=True, blank=True)
    def __str__ (self):
        return str(self.name)
       

class Stock (models.Model):
    category = models.ForeignKey (Category, on_delete=models.CASCADE, blank=True)
    item_name = models.CharField (max_length= 50, blank=True, null=True)
    quantity = models.IntegerField (default='0', blank=True, null=True)
    recieve_quantity =models.IntegerField (default='0', blank=True, null=True)
    issue_quantity = models.IntegerField (default='0', blank=True, null=True)
    issued_by =models.CharField (max_length=50, blank=True, null=True)
    issued_to = models.CharField (max_length=50, blank=True, null=True)
    recieved_by = models.CharField (max_length=50, blank=True, null=True)
    phone_number =models.CharField (max_length=50, blank=True, null=True)
    created_by = models.CharField (max_length=50, blank=True, null=True)
    reorder_level =models.IntegerField (default='0', blank=True, null=True)
    member= models.ForeignKey (Member, on_delete=models.CASCADE, )
    date =models.DateTimeField (auto_now=False, null=True, blank=True)
    timestamp =models.DateField ( auto_now_add=False, auto_now=True, null=True, blank=True)
    price =models.IntegerField (default='0', blank=True, null=True)
    total_sales =models.IntegerField ( default='0', blank=True, null=True)
    total_expenses =models.IntegerField (default='0', blank=True, null=True)
    expense = models.CharField (max_length=50, blank=True, null=True)
    net_sales =models.IntegerField (default='0', blank=True, null=True)
    start_date = models.DateField("From Date (yyyy-mm-dd)", auto_now_add=False, auto_now=False, blank=True, null=True)
    end_date = models.DateField ("To Date (yyyy-mm-dd)", auto_now_add=False, auto_now=False, blank=True, null=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.item_name +' '+ str(self.quantity)



class Expenses (models.Model):
    user= models.CharField(max_length=50)
    amount = models.IntegerField (default='0', blank=True, null=True)
    purpose = models.CharField (max_length=150, blank=True, null=True)
    timestamp = models.DateField (auto_now_add=False, auto_now=True, null=True, blank=True)
    
    def __str__(self):
        return self.purpose


    history = HistoricalRecords()
    
class Pos (models.Model):
    total_amount = models.IntegerField (default = '0', blank=True, null=True)
    sold_quantity = models.IntegerField (default = '0', blank=True, null=True)
    item_sold  = models.CharField(max_length=50)
    
    def __str__ (self):
        return self.item_sold
    
    
    history = HistoricalRecords()


class Sms (models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=50)
    message=models.TextField(max_length=1000)
    sender=models.CharField(max_length=11)
    mobiles=models.TextField(max_length=2000)
    
    def __str__ (self):
        return self.username