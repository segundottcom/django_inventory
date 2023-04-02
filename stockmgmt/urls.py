

from django.urls import path, include
from . import views
from  django.views.i18n import JavaScriptCatalog



urlpatterns=[
    path ('', views.index, name='index'),
    path ('list_items/', views.list_items, name='list_items'),
    path ('add_items/', views.add_items, name='add_items'),
    path ('new_stock', views.new_stock, name='new_stock'),
    path ('update_items/<str:pk>/', views.update_items, name='update_items'),
    path ('stock_details/<str:pk>/', views.stock_details, name='stock_details'),
    path ('issued_items/<str:pk>/', views.issued_items, name='issued_items'),
    path ('recieve_items/<str:pk>/', views.recieve_items, name='recieve_items'),
    path ('reorder_level/<str:pk>/', views.reorder_level, name='reorder_level'),
    path ('low_stock_alert/', views.low_stock_alert, name='low_stock_alert'),
    
    path ('total_sales/', views.total_sales, name='total_sales'),
    path ('expenses/', views.expenses, name='expenses'),
    path ('add_expenses/', views.add_expenses, name='add_expenses'),
    path ('select_items/', views.select_items, name='select_items'),
    path ('send_sms/', views.send_sms, name='send_sms'),
    
    path ('list_history/', views.list_history, name='list_history'),
    path ('accounts/', include ('registration.backends.default.urls')),
    
    

    path('jsi18n', JavaScriptCatalog.as_view(), name='js-catlog'),
] 

