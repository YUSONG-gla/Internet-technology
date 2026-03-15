from django.urls import path
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('category/add/', views.add_category, name='add_category'),
    path('transaction/delete/<int:transaction_id>/', views.delete_transaction, name='delete_transaction'),
    path('transaction/edit/<int:transaction_id>/', views.edit_transaction, name='edit_transaction'),
    path('set-budget/', views.set_budget, name='set_budget'),
]
