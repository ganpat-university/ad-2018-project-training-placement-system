from django.contrib.auth.models import User
from .models import *
import django_filters

class StudentFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name','email','CGPA','gender','enrollment_number','branch','placed']

class CompanyFilter(django_filters.FilterSet):
    class Meta:
        model = Company
        fields = ['name', 'criteria','email','position','package']