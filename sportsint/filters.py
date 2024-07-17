from .models import Onaylar
from django_filters import rest_framework as filters
class KisiFilter(filters.FilterSet):
    class Meta:
        model = Onaylar
        fields = ['recipient']
