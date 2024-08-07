from django.urls import path
from . views import *

urlpatterns = [
    path('', homepages, name='homepage'),
    path('destination/', destinationpage, name="destination"),
    path('packages/', packages, name="packages"),
    # path('destinationdetail/<str:destination_name>/', destinationdetail, name='destinationdetail'),
    path('destinationdetail/<int:tour_id>/', destinationdetail, name="destinationdetail"),
    path('packgesdetail/<int:tour_id>/', packgesdetail, name="packgesdetail"),
    path('register/', register, name="register"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name="logout"),
    path('about/', about_us, name="about"),
    path('contact/', contact_view, name="contact"),
    path('contact_success/', contact_success_view, name="contact_success"),  # Add this line
    path('gallery/', gallery, name="gallery"),
    path('upprofile/', profile, name="upprofile"),
    path('updateprofile/', update_profile, name="updateprofile"),
    # path('slider/', slider, name="slider"),
]

