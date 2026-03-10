from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Named URLs allow for reverse resolution in views and templates
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    # Note: dashboard route will be fully implemented in the next step
    path('dashboard/', views.dashboard, name='dashboard'),
    path('transaction/add/', views.add_transaction, name='add_transaction'),
]
