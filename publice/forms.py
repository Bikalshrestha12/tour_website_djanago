from django.forms import ModelForm
from .models import *


class DestinationForm(ModelForm):
    class Meta:
        model = Destination
        fields = "__all__"


class TourForm(ModelForm):
    class Meta:
        model = Tour
        fields = "__all__"


class BookingForm(ModelForm):
    class Meta:
        model = Booking
        fields = ["num_travelers",  "contact_no", "address", "booking_date", "payment_method"]

class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']

class About_Us_Form(ModelForm):
    class Meta:
        model = About_Us
        fields = "__all__"

class HomePage_Form(ModelForm):
    class Meta:
        model = HomePage
        fields = "__all__"

