import requests 

from datetime import date

from django.shortcuts import render, redirect

from django.contrib import messages
from .models import Stock,  HistoricalStock, HistoricalExpenses, Member
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# allows for comparing values of two django fields in a queryset
from django.db.models import F
from django.db.models import Sum  # calculates sum in a queryset
from urllib.parse import urlencode


def index(request):

    title = 'Welcome to UNIK CONNECTS INVENTORY SYSTEM'

    context = {
        'title': title,
    }
    return redirect('list_items/')


@login_required
def list_items(request):
    form = StockSearchForm(request.POST or None)
    queryset = Stock.objects.all().order_by('-timestamp')

    title = 'Item List'
    context = {
        'queryset': queryset,
        'title': title,
        'form': form


    }

    if request.method == 'POST':
        queryset = Stock.objects.filter(category__icontains=form['category'].value(),
                                        item_name__icontains=form['item_name'].value(
        )
        )
        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY'])
            instance = queryset
            for stock in queryset:
                writer.writerow(
                    [stock.category, stock.item_name, stock.quantity])
            return response
        context = {
            'form': form,
            'queryset': queryset,
            'title': title

        }

    return render(request, 'list_items.html', context)


@login_required
def add_items(request):

    queryset = Category.objects.all ()
    form = StockCreateForm(request=request)
    
    
    if request.method=='POST':
    
        
        form = StockCreateForm(request.POST or None)
    
        if form.is_valid():
            # user_id = form.cleaned_data['user_id']
    
           
            form.save()
            messages.success(request, 'Successfully saved')
            return redirect('list_items')
       
    
       
    title = 'Add Item'

    context = {

        'title': title,
        'form': form,
        
        'queryset':queryset

    }
    return render(request, 'add_items.html', context)
    
   


@login_required
def update_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = StockUpdateForm(instance=queryset)
    if request.method == "POST":
        form = StockUpdateForm(request.POST, instance=queryset)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully saved')
            return redirect('/list_items')

    context = {
        'form': form

    }
    return render(request, 'add_items.html', context)


@login_required
def new_stock(request):
    form = StockNew(request.POST or None)

    title = 'New Product Category'
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully saved')
        return redirect('/list_items')
    context = {
        'form': form,
        'title': title,


    }

    if request.method == 'POST':
        search_query = Category.objects.filter(name__icontains=form['name'].value(),
                                               )
        context = {
            'form': form,
            'search_query': search_query,
            'title': title

        }

    return render(request, 'new_stock.html', context)


@login_required
def stock_details(request, pk):
    queryset = Stock.objects.get(id=pk)
    context = {
        'queryset': queryset,

    }
    return render(request, 'stock_details.html', context)


@login_required
def low_stock_alert(request):
    queryset = Stock.objects.filter(reorder_level__gte=F('quantity'))
    context = {
        'queryset': queryset,
        'title': 'Low Stock Table'
    }
    return render(request, 'low_stock_alert.html', context)


@login_required
@login_required
def issued_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = IssueForm(request.POST or None, instance=queryset)

    if form.is_valid():

        instance = form.save(commit=False)
        instance.recieve_quantity = 0

        instance.quantity -= instance.issue_quantity
        messages.success(request, 'Sold SUCCESSFULLY. ' + str(instance.quantity) +
                         " " + str(instance.item_name) + 's now left in store')
        instance.save()

        return redirect('/stock_details/' + str(instance.id))
    context = {
        'queryset': queryset,
        'form': form,
        'username': 'Issued by ' + str(request.user)

    }
    return render(request, 'add_items.html', context)


@login_required
def recieve_items(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = RecieveForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.recieve_quantity

        messages.success(request, 'Stock updated SUCCESSFULLY. ' + str(
            instance.quantity) + " " + str(instance.item_name) + 's now  in store')
        instance.save()
        return redirect('/stock_details/' + str(instance.id))
    context = {
        'queryset': queryset,
        'form': form,
        'username': 'Recieved By ' + str(request.user)
    }
    return render(request, 'add_items.html', context)


@login_required
def reorder_level(request, pk):
    queryset = Stock.objects.get(id=pk)
    form = ReorderLevelForm(request.POST or None, instance=queryset)
    if form.is_valid():
        instance = form.save(commit=False)

        messages.success(request, 'Reorder Level for ' + str(instance.item_name) +
                         " is updated to " + str(instance.reorder_level))
        instance.save()
        return redirect('/list_items')
    context = {
        'instance': queryset,
        'form': form
    }
    return render(request, 'add_items.html', context)


@login_required
def list_history(request):
    header = 'History of Items'
    queryset = HistoricalStock.objects.all().order_by('-date')
    form = StockHistorySearchForm(request.POST or None)

    context = {

        'header': header,
        'queryset': queryset,
        'form': form
    }

    if request.method == 'POST':
        category = form['category'].value()
        queryset = HistoricalStock.objects.filter(
            item_name__icontains=form['item_name'].value(),
            timestamp__range=[form['start_date'].value(),
                              form['end_date'].value()]
        )

        if (category != ''):
            queryset = queryset.filter(category_id=category)

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME', 'QUANTITY', 'DATE'])
            instance = queryset
            for stock in queryset:
                writer.writerow([stock.category, stock.item_name,
                                stock.quantity, stock.timestamp])
            return response

        context = {
            'queryset': queryset,
            'form': form,
            'header': header


        }
    return render(request, 'list_history.html', context)


def total_sales(request):
    header = 'Total Sales'
    queryset = HistoricalStock.objects.all().order_by('-date')

    form = StockHistorySearchForm(request.POST or None)
    total_sales = ''
    total_expenses = ''
    net_sales = ''
    context = {

        'header': header,
        'queryset': queryset,
        'form': form,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'net_sales': net_sales
    }

    if request.method == 'POST':

        #category = form['category'].value()
        queryset = HistoricalStock.objects.filter(
            # item_name__icontains=form['item_name'].value(),
            timestamp__range=[form['start_date'].value(),
                              form['end_date'].value()]
        )

        total_sales = queryset.aggregate(sum=Sum('price'))['sum']

        queryset1 = HistoricalExpenses.objects.filter(
            # item_name__icontains=form['item_name'].value(),
            timestamp__range=[form['start_date'].value(),
                              form['end_date'].value()]
        )

        total_expenses = queryset1.aggregate(sum=Sum('amount'))['sum']

        if total_expenses is not None:
            net_sales = int(total_sales - total_expenses)
        else:
            net_sales = int(total_sales)

        # if  (category != ''):
            # queryset = queryset.filter (category_id=category)

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of stock.csv"'
            writer = csv.writer(response)
            writer.writerow(['CATEGORY', 'ITEM NAME',  'DATE'])
            instance = queryset
            for stock in queryset:
                writer.writerow(
                    [stock.category, stock.item_name,  stock.timestamp])
            return response

        context = {
            'queryset': queryset,
            'form': form,
            'header': header,
            'total_sales': total_sales,
            'total_expenses': total_expenses,
            'net_sales': net_sales


        }
    return render(request, 'total_sales.html', context)


@login_required
def expenses(request):

    form = ExpensesForm(request.POST or None)
    queryset = HistoricalExpenses.objects.all().order_by('-timestamp')

    context = {

        'title': 'Expenses Table',
        'form': form,
        'queryset': queryset,
        'total_expenses': " ",
        'username': " "
    }

    if request.method == 'POST':

        queryset = HistoricalExpenses.objects.filter(

            timestamp__range=[form['start_date'].value(),
                              form['end_date'].value()]
        )

        total_expenses = queryset.aggregate(Sum('amount'))

        username = str(request.user)

        if form['export_to_csv'].value() == True:
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="List of expenses.csv"'
            writer = csv.writer(response)
            writer.writerow(['PURPOSE', 'AMOUNT', 'USER', 'DATE'])
            instance = queryset
            for stock in queryset:
                writer.writerow([stock.purpose, stock.amount,
                                stock.user, stock.timestamp])
            return response

        context = {
            'queryset': queryset,
            'form': form,
            'title': 'Expenses Table',
            'total_expenses': total_expenses,
            'username': str(request.user)


        }
    return render(request, 'expenses.html', context)


@login_required
def add_expenses(request):

    form = CreateExpenses(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Successfully posted')
        return redirect('list_items')
    title = 'Add Expenses'

    context = {

        'title': title,
        'form': form

    }
    return render(request, 'add_expenses.html', context)


@login_required
def select_items(request):
    queryset = Stock.objects.all
    form = PosForm(request.POST or None)
    item_quantity = ''
    queryset1 = ''
    preview_quantity = ''
    preview_total= ''
    total_amount = 0
    item_search =''
    item_price=''
   

    if request.method == 'POST':
        
        if 'Load Stock' in request.POST:
        
            queryset1 = request.POST['selected_item']
            item_search = Stock.objects.get(item_name=queryset1)
            item_quantity = item_search.quantity
            item_price = item_search.reorder_level
        
        elif 'Accept' in request.POST:
            
            preview_quantity = request.POST ['volume']
            preview_total =int (request.POST ['amount'])
            total_amount = int (total_amount + preview_total)
           
        
    context = {

            'queryset': queryset,
            'queryset1': queryset1,
            'item_quantity': item_quantity,
            'form': form,
            'item_price': item_price,
            'preview_quantity': preview_quantity,
            'preview_total': preview_total,
            'total_amount': total_amount,
            'item_search': item_search
    }
            

    return render(request, 'select_items.html', context)

login_required

def send_sms(request):
    message = ''
    sender =''
    username= ''
    password= ''
    mobiles=''
    
    form = SmsForm (request.POST or None)
    if request.method=='POST':
    
        
        message= request.POST.get ('message')
        sender= request.POST.get ('sender')
        mobiles= request.POST.get ('mobiles')
        password= request.POST.get ('password')
        username= request.POST.get ('username')
        
        
        
       
        data = { 'username':username, 'password':password, 'message': message, 'sender': sender, 'mobiles':mobiles, }
        
        url = 'http://login.bulk-sms.ng/api/?'
        response = requests.post(url, data=data)
        return redirect ('list_items')
        
    return render (request, 'sms.html', {'form':form})
    
    

