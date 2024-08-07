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




def homepages(request):
    destination = Destination.objects.all().order_by("-id")[:8]
    homepages = HomePage.objects.all()
    user = request.user.id
    review = Review.objects.filter(user=user)

    context = {"destination": destination, "review": review, "homepages":homepages}
    return render(request, "users/index.html", context)


def destinationpage(request):
    user = request.user.id
    review = Review.objects.filter(user=user)
    destination = Tour.objects.all().order_by("-id")
    destination_filter = DestinationFilter(request.GET, queryset=destination)
    destination_result = destination_filter.qs

    context = {
        "destination_filter": destination_filter,
        "destination": destination_result,
        "review": review,
    }
    return render(request, "users/destination.html", context)

def destinationdetail(request, tour_id):
    user = request.user.id
    review = Review.objects.filter(user=user)
    destinations = Tour.objects.get(id=tour_id)
    destination = Tour.objects.all().order_by("-id")[:4]

    context = {"destinations": destinations, 
               "destination": destination,
               "review": review,
            }
    
    return render(request, "users/destinationdetail.html", context)


def packages(request):
    user = request.user.id
    review = Review.objects.filter(user=user)
    tour = Tour.objects.all().order_by("-id")
    tour_filter = TourFilter(request.GET, queryset=tour)
    tour_result = tour_filter.qs

    context = {
        "tour_filter": tour_filter,
        "tour": tour_result,
        "review": review,
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


def packgesdetail(request, tour_id):
    user = request.user.id
    review = Review.objects.filter(user=user)
    tours = Tour.objects.get(id=tour_id)
    tour = Tour.objects.all().order_by("-id")[:4]

    context = {"tours": tours, 
               "tour": tour,
               "review": review,
            }
    
    return render(request, "users/packagesdetail.html", context)



def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "User register successfully."
            )
            return redirect("/login")
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
                return redirect("/publice/publice")
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
    review = Review.objects.filter(user=user)
    about = About_Us.objects.all()
    context = {
        "about": about,
        "review":review,
    }
    return render(request, "users/about.html", context)


def gallery(request):
    user = request.user.id
    review = Review.objects.filter(user=user)
    gallery = Gallery.objects.all()
    context = {
        'gallery':gallery,
        'review':review
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


@login_required
def profile(request):
    user = User.objects.get(username=request.user)
    profile = Profile.objects.all()
    context = {"profile": profile, "user":user}
    return render(request, "users/profile.html", context)



@login_required
def update_profile(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.add_message(
                request, messages.SUCCESS, "Profile update Successfully"
            )
            return redirect("/users/profile")
        else:
            messages.add_message(request, messages.ERROR, "Failed to update profile")
            return render(request, "users/updateprofile.html", {"form": form})

    context = {"form": ProfileUpdateForm(instance=request.user)}

    return render(request, "users/updateprofile.html", context)





# def inquire(request):
#     user = request.user.id
#     review = Review.objects.filter(user=user)
#     inquire = Inquire.objects.all()
#     context = {
#         "homepages": homepages,
#         "review":review,
#     }
#     return render(request, "users/index.html", context)

def inquire(request):
    if request.method == 'POST':
        form = InquireForm(request.POST)
        if form.is_valid():

            return redirect('/inquireresult')  # Redirect to a success page

    else:
        form = InquireForm()

    return render(request, 'users/tnquirersult.html', {'form': form})


# from django.views.static import serve
# from django.conf import settings
# from django.utils.http import http_date
# from django.http import HttpResponseNotModified, Http404
# import os

# def serve_with_cache(request, path):
#     absolute_path = os.path.join(settings.STATIC_ROOT, path)
#     if not os.path.exists(absolute_path):
#         raise Http404("File not found")

#     # Get the last modified time of the file
#     statobj = os.stat(absolute_path)
#     last_modified = http_date(statobj.st_mtime)

#     if_modified_since = request.META.get('HTTP_IF_MODIFIED_SINCE')
#     if if_modified_since == last_modified:
#         return HttpResponseNotModified()

#     response = serve(request, path)
#     response['Last-Modified'] = last_modified
#     return response

# from django.http import HttpResponse
# from django.views.decorators.http import etag

# @etag(lambda x: 'etag_value')  # Replace with your etag generation function
# def my_view(request):
#     response = HttpResponse()
#     # Set some content
#     return response
