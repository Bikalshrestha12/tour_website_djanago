from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from publice.models import *
from .filter import *
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404


# Create your views here.


### ------------- ###
# ## tours/views
### ------------- ###

def homepage(request):
    destination = Destination.objects.all().order_by("-id")[:8]
    user = request.user.id
    tour = Tour.objects.filter()

    context = {"destination": destination, "tour": tour}
    return render(request, "users/index.html", context)


def destinationpage(request):
    user = request.user.id
    tour = Tour.objects.filter()
    destination = Destination.objects.all().order_by("-id")
    destination_filter = DestinationFilter(request.GET, queryset=destination)
    destination_result = destination_filter.qs

    context = {
        "destination_filter": destination_filter,
        "destination": destination_result,
        "tour": tour,
    }
    return render(request, "users/destination.html", context)


def packages(request):
    user = request.user.id
    tour = Tour.objects.filter()
    destination = Destination.objects.all().order_by("-id")
    destination_filter = DestinationFilter(request.GET, queryset=destination)
    destination_result = destination_filter.qs

    context = {
        "destination_filter": destination_filter,
        "destination": destination_result,
        "tour": tour,
    }
    return render(request, "users/packages.html", context)


# def packages(request):
#     user = request.user.id
#     destination = Destination.objects.all()
#     tour = Tour.objects.all()
#     context = {
#         "tour" : tour,
#         "destination" : destination
#     }
#     return render(request, "users/packages.html", context)


def packagesdetail(request, destination_id):
    user = request.user.id
    tour = Tour.objects.filter(user=user)
    destinations = Destination.objects.get(Destination, id=destination_id)
    destination = Destination.objects.all().order_by("-id")[:4]

    context = {"destinations": destinations, 
               "destination": destination, 
               "tour": tour
            }
    
    return render(request, "users/packagesdetail.html", context)




def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "User register successfully."
            )
            return redirect("/users/register")
        else:
            messages.add_message(request, messages.ERROR, "Kindly check all the field.")
            return render(request, "users/register.html", {"form": form})

    context = {"form": RegisterForm}
    return render(request, "users/register.html", context)


def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            users = authenticate(
                request, username=data["username"], password=data["password"]
            )

            if users is not None:
                login(request, users)
                if users.is_staff:
                    return redirect("/admins")
                else:
                    return redirect("/")
                return redirect("/products/products")
            else:
                messages.add_message(
                    request, messages.ERROR, "Please provide correct credential"
                )
                return render(request, "users/login.html", {"form": form})
    # form = LoginForm
    # context={
    #     'form':form
    # }
    return render(request, "users/login.html", {"form": LoginForm})


def logout_user(request):
    logout(request)
    return redirect("/")




def about_us(request):
    user = request.user.id
    tour = Tour.objects.filter()
    context = {
        "tour": tour,
    }
    return render(request, "users/about.html", context)

def gallery(request):
    gallery = Destination.objects.all()
    context = {
        'gallery':gallery
    }
    return render(request, "users/gallery.html", context)



def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Send email
            try:
                # Attempt to send email
                send_mail(
                    f'Contact Form Submission - {subject}',
                    f'Name: {name}\nEmail: {email}\nMessage: {message}',
                    'shresthabikal44@gmail.com',
                    ['shresthabikal44@gmail.com'],
                    fail_silently=False,
                )
            except Exception as e:
                # Print detailed exception information
                print(f"Error sending email: {e}")
                # Optional: Log the error for further analysis
                # logger.error(f"Error sending email: {e}")

            return redirect('/contact_success')  # Redirect to a success page

    else:
        form = ContactForm()

    return render(request, 'users/contact.html', {'form': form})



def contact_success_view(request):
    return render(request, 'users/contact_success.html')  # Replace 'users/contact_success.html' with your actual template path
