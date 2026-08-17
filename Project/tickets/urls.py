from django.urls import path
from . import views

urlpatterns = [
    path('',views.ticket_list,name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('detail/<int:id>',views.ticket_detail,name='detail'),
    path('create/', views.ticket_create, name='create'),

]
