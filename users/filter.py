import django_filters
from publice.models import *
from django_filters import CharFilter

# class ProductFilter(django_filters.FilterSet):
#     product_contain_name = CharFilter(field_name='product_name', lookup_expr='icontains')
#     class Meta:
#         model = Product
#         fields = ""
#         exclude = ['product_price','stock', 'image']


## tours/filter
class DestinationFilter(django_filters.FilterSet):
    destination_contain_name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Destination
        fields = ""
        exclude = ['duration_days','price', 'title']