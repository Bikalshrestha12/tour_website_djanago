from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# tours/models.py
from django.db import models
from django.contrib.auth.models import User


class Destination(models.Model):
    location = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="static/uploads")

    def __str__(self):
        return self.name


class Tour(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='tours')
    location = models.CharField(max_length=150, null=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.IntegerField()
    duration_days = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    max_person = models.IntegerField(blank=True, null=True)
    image = models.ImageField(upload_to="static/uploads", null=True)

    def __str__(self):
        return self.title


class Booking(models.Model):
    PAYMENT = {
        ('Cash on delivery', 'Cash on delivery'),
        ('Esewa', 'Esewa'),
    }
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_booked = models.DateTimeField(auto_now_add=True)
    num_travelers = models.IntegerField()
    total_cost = models.IntegerField()
    contact_no = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    payment_method = models.CharField(choices=PAYMENT, max_length=200, null=True)
    status = models.CharField(default='Pending', max_length=200)
    payment_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


class Review(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=zip(range(1, 6), range(1, 6)))
    comment = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.tour.title}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email_address = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255)
    citizenship = models.ImageField(upload_to="static/citizen", blank=True)
    passport = models.ImageField(upload_to="static/citizen", blank=True)
    # Add more fields as needed

    def __str__(self):
        return self.user.username

class Gallery(models.Model):
    image = models.ImageField(upload_to="static/gallery")