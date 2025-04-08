from django.urls import path
from . import views 

urlpatterns = [
    path('user_dash',views.user_dash,name='user_dashboard'),
    path('digital',views.digital_dash,name='digital_dashboard'),
    path('painting',views.paint_dash,name='paint_dashboard'),
    path('sclupture',views.sclupture_dash,name='sclupture_dashboard'),
    path('doodling',views.doodling_dash,name='doodling_dashboard'),

    path('myorders',views.myorders,name='myorders_dashboard'),


    path('search',views.search,name='search'),

    path("details/<int:id>/", views.details_page, name="details"),
    path("artist_profile/<int:id>/",views.artist_profile_page,name="artist_profile"),

    path('live_search/', views.live_search, name='live_search'),

    path('stripe.com/payment/<int:id>/', views.paymentpage, name='paymentpage'),

    path('process-payment/', views.process_payment, name='process_payment'),

    path("reviewpage/<int:id>/",views.reviewpage,name="reviewpage"),

    path('addtocart/<int:id>/', views.addtocart, name='addtocart'),

    path('mycart/', views.mycart, name='mycart'),

    path('chatsystem/<int:receiver_id>/', views.chatsystem, name='chatsystem'),




    







]