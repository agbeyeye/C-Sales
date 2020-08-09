from django.db import models
from django.contrib.auth.models import User

#collection of cars submitted by users
class Car(models.Model):
	seller			=	models.ForeignKey(User, max_length=100, on_delete=models.CASCADE)
	sellerType		=	models.CharField( max_length=60)
	Id	        	=   models.CharField(primary_key = True , max_length=60)
	make        	=   models.CharField(max_length=60)
	model=   models.CharField(max_length=60)
	Year		    =   models.CharField(max_length=60)
	trim            =   models.CharField(max_length=60)
	engine		    =   models.CharField(max_length=60)
	transmission    =   models.CharField(max_length= 20)
	drivetrain	    =   models.CharField(max_length=60)
	fuelType		=   models.CharField(max_length=60)
	askingPrice	    =   models.CharField("Asking Price",max_length=60)
	priceNegotiation=   models.BooleanField(default=False)
	vin			    =   models.CharField(max_length=100)
	title			=	models.CharField(max_length=60)
	milleage	    =   models.CharField(max_length=60)
	exteriorColor   =   models.CharField(max_length=60)
	interiorColor   =   models.CharField(max_length=60)
	wheelAlignment  =   models.CharField(max_length=60)
	country		    =   models.CharField(max_length=60)
	state		    =   models.CharField(max_length=60)
	zipCode		    =   models.CharField(max_length=60)
	upgrade		    =   models.TextField(null=True)
	repair		    =   models.TextField(null=True)
	rebuildingLink	=	models.CharField(max_length=90, null=True,blank=True)
	recentService   =   models.TextField(null=True)
	alignmentTest	=	models.BooleanField(default=False)
	flaws		    =   models.TextField(null=True,blank=True)
	extraInfo	    =   models.TextField("Additional Information",null=True,blank=True)
	contact			=	models.CharField(max_length=30)
	hideContact		=	models.BooleanField(default=False)
	financing		=	models.BooleanField(default=False)
	serviceContract	=	models.BooleanField(default=False)
	termsAndConditionsAccepted= models.BooleanField(default=False)
	views			=	models.IntegerField(default=0)
	enlisted_days   =  models.IntegerField(default=0)
	date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)
	sold			=	models.BooleanField(default=False)

	def __str__(self):
		return self.Id

#photos of cars
class CarImages(models.Model):
	image 			=	models.ImageField(upload_to ='uploads/images/')
	car				=	models.ForeignKey(Car, on_delete=models.CASCADE)
	#date			=	models.DateTimeField(auto_now_add=True, auto_now=False)

	# def __str__(self):
	# 	return self.ca

#repair photos of car
class RepairedCarImages(models.Model):
	image 			=	models.ImageField(upload_to ='uploads/repairs/')
	car				=	models.ForeignKey(Car, on_delete=models.CASCADE)
	# date			=	models.DateTimeField(auto_now_add=True, auto_now=False)

	# def __str__(self):
	# 	return self.image


# Users' watchlist
class watchlist(models.Model):
	user			=	models.ForeignKey(User,on_delete=models.CASCADE)
	car 			=	models.ForeignKey(Car,on_delete=models.CASCADE)
	# date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)

	# def __str__(self):
	# 	return self.user.email




# Direct messages
class Messages(models.Model):
	sender	=	models.ForeignKey(User,on_delete=models.CASCADE)
	recepientEmail	=	models.CharField(max_length=60)
	content			=	models.TextField()
	date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)
	readStatus		=	models.BooleanField(default=False)

	def __str__(self):
		return self.content



# Users' Comments
class Comments(models.Model):
	sender	=	models.ForeignKey(User,on_delete=models.CASCADE)
	content			=	models.TextField()
	date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)
	readStatus		=	models.BooleanField(default=False)

	def __str__(self):
		return self.content
