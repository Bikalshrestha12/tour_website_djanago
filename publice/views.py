from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from django.http import *
from .models import *
from .forms import *

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


# class EsewaView(View):
#     def get(self, request, *args, **kwargs):
#         o_id = request.GET.get("o_id")
#         c_id = request.GET.get("c_id")
#         tour = Tour.objects.get(id=c_id)
#         booking = Booking.objects.get(id=o_id)

#         uuid_val = uuid.uuid4()

#         def genSha256(key, message):
#             key = key.encode("utf-8")
#             message = message.encode("utf-8")

#             hmac_sha256 = hmac.new(key, message, hashlib.sha256)

#             digest = hmac_sha256.digest()

#             signature = base64.b64encode(digest).decode("utf-8")
#             return signature

#         secret_key = "8gBm/:&EnhH.1/q"
#         data_to_sign = f"total_amount={booking.total_price},transaction_uuid={uuid_val},product_code=EPAYTEST"

#         result = genSha256(secret_key, data_to_sign)

#         data = {
#             "amount": booking.Product.product_price,
#             "total_amount": booking.total_price,
#             "transaction_uuid": uuid_val,
#             "product_code": "EPAYTEST",
#             "signature": result,
#         }
#         context = {"booking": booking, "data": data, "tour": tour}
#         return render(request, "users/esewa_payment.html", context)


# import json


# @login_required
# def esewa_verify(request, order_id, cart_id):
#     if request.method == "GET":
#         data = request.GET.get("data")
#         decoded_data = base64.b64decode(data).decode("utf-8")
#         map_data = json.loads(decoded_data)
#         booking = Booking.objects.get(id=order_id)
#         tour = Tour.objects.get(id=cart_id)

#         if map_data.get("status") == "COMPLETE":
#             booking.payment_status = True
#             booking.save()
#             tour.delete()
#             messages.add_message(request, messages.SUCCESS, "Payment Successful")
#             return redirect("/products/my_order")
#         else:
#             messages.add_message(request, messages.ERROR, "Failed to Make a Payment")
# return redirect("/products/my_order")


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
    return render(
        request, "publice/destination_list.html", {"destination": destination}
    )


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
    destination = destination.objects.get(name=name)
    if request.method == "POST":
        form = DestinationForm(request.POST, request.FILES, instance=destination)
        if form.is_valid():
            form.save()
            return redirect("tour_list")
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
    return render(
        request, "publice/destination_delete.html", {"destination": destination}
    )


def book_tour(request, tour_id):
    user = request.user
    tour = Tour.objects.get(id=tour_id)

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            num_travelers = request.POST.get("num_travelers")
            price = tour.price
            total_cost = int(num_travelers) * int(price)
            contact_no = request.POST.get("contact_no")
            address = request.POST.get("address")
            payment_method = request.POST.get("payment_method")
            book = Booking.objects.create(
                tour=tour,
                user=user,
                total_cost=total_cost,
                contact_no=contact_no,
                address=address,
                payment_method=payment_method,
            )

            # Save the form data to the database

            # Redirect to a success page or any other page
            # return redirect(
            #     "/products/booking_form"
            # )  # Replace with your URL name or path
    context = {"form": BookingForm}

    return render(request, "publice/booking_form.html", context)


@login_required
@admin_only
def user(request):
    user = User.objects.all()
    context = {"user": user}
    return render(request, "publice/user.html", context)
