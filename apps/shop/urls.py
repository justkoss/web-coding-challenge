from django.conf.urls import url
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
    path('index', views.index, name='index'),
    path('addPreferredShop/<int:id>/', views.addPreferredShop, name='addPreferredShop'),
    path('addDislikedShop/<int:id>/', views.addDislikedShop, name='addDislikedShop'),
    path('deletePreferredShop/<int:id>/', views.deletePreferredShop, name='deletePreferredShop'),
    path('PreferredShop', views.preferredShop, name='preferredShop'),
    url(r'^save_events_json/$', views.save_events_json, name='save_events_json'),

]
