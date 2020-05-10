from .models import *
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = ['enrollment_number','first_name','last_name','email','phone','gender','branch','birth_date','permanent_address','current_address','aadhaar_number','HSC_board','HSC_year','HSC_marks','HSC_school_name','SSC_board','SSC_year','SSC_marks','SSC_school_name','active_back','passive_back','course','college_name','university','passing_year','CGPA','lock','placed_company_id','placed']

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [f.name for f in Company._meta.fields]

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('enrollment_number', 'description','document', )

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'slug','content', )
