
from django.shortcuts import render, redirect
from django.http import *
from .models import *
from .forms import *
from users.forms import *

# from users.forms import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from users.auth import admin_only
from django.urls import reverse
from django.views import View
import decimal


import hmac  # cryptography algorithm
import hashlib  # encrypt data
import uuid  # to generate random string
import base64

# Create your views here.



@login_required
@admin_only
def tour_list(request):
    tour = Tour.objects.all()
    return render(request, "publice/tour_list.html", {"tour": tour})


@login_required
@admin_only
def tour_detail(request, pk):
    tour = Tour.objects.get(pk=pk)
    return render(request, "publice/tour_detail.html", {"tour": tour})


@login_required
@admin_only
def tour_create(request):
    if request.method == "POST":
        form = TourForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("tour_list")
    else:
        form = TourForm()
    return render(request, "publice/tour_form.html", {"form": form})


@login_required
@admin_only
def tour_update(request, pk):
    destination = Tour.objects.get(pk=pk)
    if request.method == "POST":
        form = TourForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect("tour_list")
    else:
        form = TourForm(instance=destination)
    return render(request, "publice/tour_form.html", {"form": form})


@login_required
@admin_only
def tour_delete(request, pk):
    tour = Tour.objects.get(pk=pk)
    if request.method == "POST":
        tour.delete()
        return redirect("tour_list")
    return render(request, "publice/tour_confirm_delete.html", {"tour": tour})


@login_required
@admin_only
def destination_list(request):
    destination = Destination.objects.all()
    return render(request, "publice/destination_list.html", {"destination": destination})


@login_required
@admin_only
def destination_detail(request, pk):
    desstination = Destination.objects.get(pk=pk)
    return render(
        request, "publice/destination_detail.html", {"desstination": desstination}
    )


@login_required
@admin_only
def destination_create(request):
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("destination_list")
    else:
        form = DestinationForm()
    return render(request, "publice/destination_form.html", {"form": form})


@login_required
@admin_only
def destination_update(request, name):
    destination = Destination.objects.get(name=name)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect("destination_list")
    else:
        form = DestinationForm(instance=destination)
    return render(request, "publice/destination_form.html", {"form": form})


@login_required
@admin_only
def destination_delete(request, pk):
    destination = Destination.objects.get(pk=pk)
    if request.method == "POST":
        destination.delete()
        return redirect("destination_list")
    return render( request, "publice/destination_delete.html", {"destination": destination})

@login_required
def book_tour(request, tour_id):
    user = request.user
    tour = Tour.objects.get(id=tour_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            num_travelers = request.POST.get("num_travelers")
            price = tour.price
            duration_days = tour.duration_days
            total_cost = int(num_travelers) * int(price) *int(duration_days)
            booking_date = request.POST.gey("booking_date")
            contact_no = request.POST.get("contact_no")
            address = request.POST.get("address")
            payment_method = request.POST.get("payment_method")
            book = Booking.objects.create(
                tour=tour,
                user=user,
                num_travelers = num_travelers,
                total_cost=total_cost,
                booking_date = booking_date,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
            )
            if book.payment_method == "Cash on delivery":
                item = Tour.objects.get(id=tour_id)
                # item.delete()
                messages.add_message(
                    request, messages.SUCCESS, "Booking Successfull be ready with Cash"
                )
                return redirect("/publice/mybook")
            
            elif book.payment_method == "Esewa":
                return redirect(reverse("esewaform") + "?o_id=" + str(book.id) + "&c_id=" + str(tour.id))
            else:
                messages.add_message(
                    request, messages.ERROR, "Kindly check the payment method"
                )
                return render(request, "users/tours.html", {"form": form})

            # Save the form data to the database

            # Redirect to a success page or any other page
            # return redirect(
            #     "/products/booking_form"
            # )  # Replace with your URL name or path
    context = {"form": BookingForm}

    return render(request, "publice/booking_form.html", context)




class EsewaView(View):
    def get(self, request, *args, **kwargs):
        o_id = request.GET.get("o_id")
        c_id = request.GET.get("c_id")
        tour = Tour.objects.get(id=c_id)
        booking = Booking.objects.get(id=o_id)

        uuid_val = uuid.uuid4()

        def genSha256(key, message):
            key = key.encode("utf-8")
            message = message.encode("utf-8")

            hmac_sha256 = hmac.new(key, message, hashlib.sha256)

            digest = hmac_sha256.digest()

            signature = base64.b64encode(digest).decode("utf-8")
            return signature

        secret_key = "8gBm/:&EnhH.1/q"
        data_to_sign = f"total_amount={booking.total_cost},transaction_uuid={uuid_val},product_code=EPAYTEST"

        result = genSha256(secret_key, data_to_sign)

        data = {
            "amount": booking.tour.price,
            "total_amount": booking.total_cost,
            "transaction_uuid": uuid_val,
            "product_code": "EPAYTEST",
            "signature": result,
        }
        context = {"booking": booking, "data": data, "tour": tour}
        return render(request, "users/esewa_payment.html", context)


import json


@login_required
def esewa_verify(request, book_id, tour_id):
    if request.method == "GET":
        data = request.GET.get("data")
        decoded_data = base64.b64decode(data).decode("utf-8")
        map_data = json.loads(decoded_data)
        booking = Booking.objects.get(id=tour_id)
        tour = Tour.objects.get(id=book_id)

        if map_data.get("status") == "COMPLETE":
            booking.payment_status = True
            booking.save()
            tour.delete()
            messages.add_message(request, messages.SUCCESS, "Payment Successful")
            return redirect("/users/mybook")
        else:
            messages.add_message(request, messages.ERROR, "Failed to Make a Payment")
    return redirect("/users/mybook")




@login_required
def my_book(request):
    user = request.user
    items = Booking.objects.filter(user=user)

    context = {"item": items}
    return render(request, "users/mybook.html", context)
# @login_required
# def my_book(request, tour_id):
#     user = request.user
#     tour = Tour.objects.get(id=tour_id)
#     check_presence = Booking.objects.filter(user=user, tour=tour)
#     if check_presence:
#         messages.add_message(request, messages.ERROR, "Booking is alreay present in cart")
#         return redirect("/publice/mybook")
#     else:
#         booking = Booking.objects.create(user=user, tour=tour) 
#         if booking:
#             messages.add_message(request, messages.SUCCESS, "Booking add successfully")
#             return redirect("/publice/mybook")
#         else:
#             messages.add_message(request, messages.ERROR, "Please try again")


@login_required
def remove_book_item(request, book_id):
    item = Booking.objects.get(id=book_id)
    item.delete()
    messages.add_message(request, messages.ERROR, "Item removed successfully")
    return redirect("/publice/mybook")


@login_required
@admin_only
def user(request):
    user = User.objects.all()
    context = {"user": user}
    return render(request, "publice/user.html", context)


@login_required
@admin_only
def gallery_list(request):
    gallery = Gallery.objects.all()
    return render(request, "publice/gallery_list.html", {"gallery": gallery})


@login_required
@admin_only
def gallery_form(request):
    if request.method == 'POST':
        form = GalleryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # instance = form.save()
            return redirect("gallery_list")
    else:
        form = GalleryForm()
    return render(request, "publice/gallery_form.html", {"form": form})

@login_required
@admin_only
def gallery_delete(request, pk):
    gallery = Gallery.objects.get(pk=pk)
    if request.method == "POST":
        gallery.delete()
        return redirect("gallery_list")
    return render( request, "publice/gallery_delete.html", {"gallery": gallery})



@login_required
@admin_only
def about_list(request):
    about_us = About_Us.objects.all()
    return render(request, "publice/about_us_list.html", {"about_us": about_us})


@login_required
@admin_only
def about_form(request):
    if request.method == 'POST':
        form = About_Us_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # instance = form.save()
            return redirect("about_us_list")
    else:
        form = About_Us_Form()
    return render(request, "publice/about_us_form.html", {"form": form})


@login_required
@admin_only
def about_update(request, pk):
    destination = About_Us.objects.get(pk=pk)
    if request.method == "POST":
        form = About_Us_Form(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect("about_us_list")
    else:
        form = About_Us_Form(instance=destination)
    return render(request, "publice/about_us_form.html", {"form": form})

@login_required
@admin_only
def about_delete(request, pk):
    about_us = About_Us.objects.get(pk=pk)
    if request.method == "POST":
        about_us.delete()
        return redirect("gallery_list")
    return render( request, "publice/about_us_delete.html", {"about_us": about_us})


@login_required
@admin_only
def home_list(request):
    homepage = HomePage.objects.all()
    return render(request, "publice/homepage.html", {"homepage": homepage})


@login_required
@admin_only
def homepages_form(request):
    if request.method == 'POST':
        form = HomePage_Form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # instance = form.save()
            return redirect("homepage")
    else:
        form = HomePage_Form()
    return render(request, "publice/homepage_form.html", {"form": form})


@login_required
@admin_only
def homepage_update(request, pk):
    destination = HomePage.objects.get(pk=pk)
    if request.method == "POST":
        form = HomePage_Form(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect("homepage")
    else:
        form = HomePage_Form(instance=destination)
    return render(request, "publice/homepage_form.html", {"form": form})

def booking(request):
    bookings = Booking.objects.all()
    context = {
        "booking":bookings
    }
    return render(request, "publice/bookings.html", context)


@login_required
def add_to_favoriteplace(request, tour_id):
    user = request.user
    tour = Tour.objects.get(id=tour_id)
    check_presences = Booking.objects.filter(user=user, tour=tour)
    if check_presences:
        messages.add_message(request, messages.ERROR, "Your Favorite place is alreay present in cart")
        return redirect("/publice/favorite")
    else:
        booking = Booking.objects.create(user=user, tour=tour) 
        if booking:
            messages.add_message(request, messages.SUCCESS, "Your Favorite place add successfully")
            return redirect("/publice/favorite")
        else:
            messages.add_message(request, messages.ERROR, "Please try again")


@login_required
def remove_favoriteplace_item(request, book_id):
    item = Booking.objects.get(id=book_id)
    item.delete()
    messages.add_message(request, messages.ERROR, "Item removed successfully")
    return redirect("/publice/favorite")
