from django.urls import path
from . import views

urlpatterns = [
    path("tour_list/", views.tour_list, name="tour_list"),
    path("tour/<int:pk>/", views.tour_detail, name="tour_detail"),
    path("tour_create/", views.tour_create, name="tour_create"),
    path("tour/<int:pk>/edit/", views.tour_update, name="tour_update"),
    path("tour/<int:pk>/delete/", views.tour_delete, name="tour_delete"),
    path("destination_list/", views.destination_list, name="destination_list"),
    path("destination/<int:pk>/", views.destination_detail, name="destination_detail"),
    path("destination_create/", views.destination_create, name="destination_create"),
    path("todestination/<str:name>/edit/", views.destination_update,  name="destination_update"),
    path("destination/<int:pk>/delete/", views.destination_delete, name="destination_delete"),
    # path('esewaform/', views.EsewaView.as_view(), name="esewaform"),
    # path('esewaverify/<int:tour_id>/<int:booking_id>', views.esewa_verify, name="esewaverify"),
    path("booktour/<int:tour_id>/", views.book_tour, name="booktour"),
    path("user/", views.user, name="user"),
    path('gallery_list/', views.gallery_list, name='gallery_list'),
    path('gallery_form/', views.gallery_form, name="gallery_form"),
    path('gallery_delete/<int:pk>/delete/', views.gallery_delete, name="gallery_delete"),
]
