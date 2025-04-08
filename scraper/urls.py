from django.urls import path
from . import views

urlpatterns = [
    path('events/<int:city_id>/', views.scrape_events, name="scrape_events"),
    path('sclupture/', views.sclupture, name="sclupture_show"),    
    path('painting/', views.painting, name="painting"),    

]
