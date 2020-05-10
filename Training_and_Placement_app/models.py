from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User


class Company(models.Model):

	c_id		=	models.AutoField(primary_key=True)
	name		=	models.CharField(max_length=40,blank=False)
	criteria	=	models.FloatField(null=False, blank=False)
	contact_number = models.IntegerField(null=True,blank=True)
	email       =		models.EmailField(max_length=50,null=False,blank=False)
	address =		models.CharField(max_length=1000,null=True,blank=True)
	position =		models.CharField(max_length=1000,blank=False)
	package		=	models.FloatField(blank=True,null=True)
	hired_count = 	models.IntegerField(null=True,blank=True,default=0)
	website		=	models.CharField(max_length=1000,blank=True)
	required_recruitment = models.IntegerField(null=False,blank=False)
	other_details=	models.TextField(max_length=1000,null=True,blank=True)

	def __str__(self):
		if self.position:
			return  self.name + "("+ self.position + ")"
		else:
			return  self.name

	def get_absolute_url(self):
		return reverse('company_edit', kwargs={'pk': self.pk})


GENDER = (
    ('Male','male'),
    ('Female','female'),
)


class Student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	s_id		=		models.AutoField(primary_key=True)
	enrollment_number		= 		models.IntegerField(unique=True,null=False,blank=False)
	first_name 	= 	models.CharField(max_length=100, blank=False)
	last_name 	= 	models.CharField(max_length=100, blank=False)
	email       =		models.EmailField(max_length=50,unique=True,blank=False)
	phone       =		models.CharField(max_length=100,null=True,blank=False)
	gender      =		models.CharField(max_length=100, choices=GENDER,blank=False)
	branch		=		models.CharField(max_length=100)
	birth_date	=		models.DateField(null=True,blank=True)
	permanent_address =		models.CharField(max_length=1000,null=True,blank=True)
	current_address =		models.CharField(max_length=1000,null=True,blank=True)
	aadhaar_number=		models.CharField(max_length=500,null=True,blank=True)
	HSC_board =		models.CharField(max_length=500,null=True,blank=True)
	HSC_year = 	models.CharField(max_length=100,null=True,blank=True)
	HSC_marks	=		models.FloatField(null=True,blank=True)
	HSC_school_name=	models.CharField(max_length=1000,null=True,blank=True)
	SSC_board= 	models.CharField(max_length=500,null=True,blank=True)
	SSC_year = 	models.CharField(max_length=100,null=True,blank=True)
	SSC_marks=		models.FloatField(null=True,blank=True)
	SSC_school_name=models.CharField(max_length=1000,null=True,blank=True)
	active_back	 =		models.IntegerField(null=True,default=0)
	passive_back = 		models.BooleanField(null=True,default=False)
	course = models.CharField(max_length=10, null=True, blank=True, default="B.TECH")
	college_name = models.CharField(max_length=1000,null=True,blank=True, default="ICT")
	university = models.CharField(max_length=1000,null=True,blank=True, default="Ganpat University")
	passing_year = models.CharField(max_length=100,null=True,blank=True)
	CGPA= models.FloatField(null=False,blank=False)
	placed		=		models.BooleanField(null=True,default=False)
	lock		=		models.BooleanField(null=True,default=False)
	placed_company_id = models.CharField(max_length=100,null=True,blank=True)

	def __str__(self):
		return self.first_name+" "+self.last_name
		
	def get_absolute_url(self):
		return reverse('student_edit', kwargs={'pk': self.pk})


def user_directory_path(instance, filename):
    return '{0}/{1}'.format(instance.user.email, filename)

class Document(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	enrollment_number = models.CharField(max_length=255, blank=False)
	description = models.CharField(max_length=255, blank=True)
	document = models.FileField(upload_to=user_directory_path)
	uploaded_at = models.DateTimeField(auto_now_add=True)
	

class Suggested(models.Model):
	sc_id		=		models.AutoField(primary_key=True)
	std 	= 		models.ForeignKey(Student, on_delete=models.CASCADE)
	cmp 	= 		models.ForeignKey(Company, on_delete=models.CASCADE)


STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete= models.CASCADE,related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now= True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title