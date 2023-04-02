from django.contrib import admin
from .forms import *
from .models import *
from simple_history.admin import SimpleHistoryAdmin


class AdminCreateForm (admin.ModelAdmin):
    
        
    list_display = ['category', 'item_name', 'quantity', 'price']
    
    form = StockCreateForm 
    search_fields = ['category', 'name']
    list_filter = ['category']
    
class AdminExpensesForm (admin.ModelAdmin):
    list_display = ['purpose', 'amount', 'user']


class AdminPosForm (admin.ModelAdmin):
    
    list_display = ['item_sold', 'sold_quantity', 'total_amount']
   



    

admin.site.register (Stock, AdminCreateForm)

admin.site.register (Pos, AdminPosForm)

admin.site.register (Expenses, AdminExpensesForm)

admin.site.register (Category, SimpleHistoryAdmin)

admin.site.register (Sms)

# Register your models here.
