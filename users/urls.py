from django.urls import path
from . views import *

urlpatterns = [
    
    path('', homepage, name='homepage'),
    path('destination/', destinationpage, name="destination"),
    path('packages/', packages, name="packages"),
    path('packagesdetail/<int:tour_id>/', packagesdetail, name="packagesdetail"),
    path('register/', register, name="register"),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name="logout"),
    path('about/', about_us, name="about"),
    path('contact/', contact_view, name="contact"),
    path('contact_success/', contact_success_view, name="contact_success"),  # Add this line
    path('gallery/', gallery, name="gallery"),

]