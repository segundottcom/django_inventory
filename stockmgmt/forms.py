from django.http import HttpResponse
from django import forms
from .models import *
import csv
from django.utils import timezone
from datetime import datetime
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget


class StockCreateForm (forms.ModelForm):
    
    user_id = forms.IntegerField(widget=forms.HiddenInput())
    class Meta:
        model = Stock
        fields = ['category', 'item_name',  'price', 'member']
    
    def __init__(self, *args, **kwargs):
        
        self.request = kwargs.pop('request')
        super(StockCreateForm, self).__init__(*args, **kwargs)
        self.fields['member'].queryset = Member.objects.filter(
            user=self.request.user)



    
            
        
class StockSearchForm (forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'price']


class StockUpdateForm (forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'quantity', 'price']
        

class StockNew (forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        
    def clean_category (self):
        name = self.cleaned_data.get ('name')
        if not name:
            raise forms.ValidationError ('This field is required')
        for instance in Category.objects.all():
            if instance.name==name:
                raise forms.ValidationError ('Category name  already exit')
        return name

class StockHistorySearchForm (forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    start_date = forms.DateField(widget= AdminDateWidget(), required=False)
    end_date = forms.DateField(widget= AdminDateWidget(), required=False)
    class Meta:
        model = Stock
       
        fields = ['category', 'item_name']


    
class StockSearchForm (forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    class Meta:
        model = Stock
        fields = ['category', 'item_name', 'price']

    
    
class IssueForm (forms.ModelForm):
    class Meta:
        model= Stock
        fields = ['issue_quantity', 'issued_to']
        

class RecieveForm (forms.ModelForm):
    class Meta:
        model=Stock
        fields= ['recieve_quantity']
 
 
class ReorderLevelForm (forms.ModelForm):
    class Meta:
      model= Stock
      fields= ['reorder_level']  
      

class CreateExpenses (forms.ModelForm):
    class Meta:
        model = Expenses
        fields = ['purpose', 'amount']

     
class ExpensesForm (forms.ModelForm):
    export_to_csv = forms.BooleanField(required=False)
    start_date = forms.DateField(widget= AdminDateWidget(), required=False)
    end_date = forms.DateField(widget= AdminDateWidget(), required=False)
    class Meta:
        model = Expenses
        fields = [  'start_date', 'end_date']



    
class PosForm (forms.ModelForm):
    
   
    
    class Meta:
        model = Stock
        fields = [ 'quantity', 'price']
  
  
class SmsForm (forms.ModelForm):
    
   
    
    class Meta:
        model = Sms
        fields = [ 'username', 'password', 'message', 'sender', 'mobiles']
  