from django.urls import path
from . import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('artist_dash',views.artist_reg,name='artist_dashboard'),
    path("artist",views.artist_page,name="artist"),
    path("art_upload",views.art_upload,name="art_upload"),
    path('update_delivery/<int:order_id>/', views.update_delivery_date, name='update_delivery_date'),



  path('get_user_list/', views.get_user_list, name='get_user_list'),
    path('get_user_messages/<int:other_user_id>/', views.get_user_messages, name='get_user_messages'),
    path('send_message/', views.send_message, name='send_message'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
