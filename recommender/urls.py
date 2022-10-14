from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    #path('', views.Index.as_view(), name='index'),
    path('about/', views.ReloadView.as_view, name='reload'),
    path('contact/', views.ContactView.as_view, name= 'contact')
    
]