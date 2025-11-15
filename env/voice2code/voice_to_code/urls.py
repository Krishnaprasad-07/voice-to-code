from django.urls import path
from . import views

urlpatterns = [
    
    path('voice2code', views.voice2code, name='voice2code'),
    path('save_code',views.save_code,name='save_code'),
]