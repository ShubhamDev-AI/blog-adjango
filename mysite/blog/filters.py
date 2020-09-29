# from django.contrib.auth.models import User
# import django_filters

# class UserFilter(django_filters.FilterSet):
#     first_name = django_filters.CharFilter(lookup_expr='icontains')
#     class Meta:
#         model = User
#         fields = ['username', 'first_name', 'last_name', ]

from django import forms
from django.contrib.auth.models import User, Group

import django_filters


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    groups = django_filters.ModelMultipleChoiceFilter(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'groups']

