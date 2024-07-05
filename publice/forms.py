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
        fields = ["num_travelers", "total_cost", "contact_no", "address", "payment_method"]

class GalleryForm(ModelForm):
    class Meta:
        model = Gallery
        fields = ['image']