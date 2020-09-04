from django.db import models
from django.contrib.auth.models import User
import datetime


#user profile
class UserProfile(models.Model):
	user = models.OneToOneField(User, related_name='user',on_delete=models.CASCADE)
	photo = models.ImageField(verbose_name=("Profile Picture"),upload_to ='uploads/profile_photos/')
	def  __str__(self):
		return self.user.username

#collection of cars submitted by users
class Car(models.Model):
	seller			=	models.ForeignKey(User, max_length=100, on_delete=models.CASCADE)
	name 			=	models.CharField(max_length=160,blank=True, null=True)
	sellerType		=	models.CharField( max_length=60)
	make        	=   models.CharField(max_length=60)
	model=   models.CharField(max_length=60)
	Year		    =   models.CharField(max_length=60)
	trim            =   models.CharField(max_length=60)
	engine		    =   models.CharField(max_length=60)
	transmission    =   models.CharField(max_length= 120)
	drivetrain	    =   models.CharField(max_length=160)
	fuelType		=   models.CharField(max_length=60)
	askingPrice	    =   models.CharField("Asking Price",max_length=60)
	priceNegotiation=   models.BooleanField(default=False)
	vin			    =   models.CharField(max_length=100)
	title			=	models.CharField(max_length=60)
	milleage	    =   models.CharField(max_length=60)
	exteriorColor   =   models.CharField(max_length=160)
	interiorColor   =   models.CharField(max_length=160)
	wheelAlignment  =   models.CharField(max_length=60)
	country		    =   models.CharField(max_length=60)
	state		    =   models.CharField(max_length=60)
	city		    =   models.CharField(max_length=60,blank=True, null=True)
	zipCode		    =   models.CharField(max_length=60)
	upgrade		    =   models.TextField(null=True,blank=True)
	repair		    =   models.TextField(null=True,blank=True)
	rebuildingLink	=	models.CharField(max_length=160, null=True,blank=True)
	videoLinks = models.CharField(max_length=6000, null=True, blank=True)
	recentService   =   models.TextField(null=True,blank=True)
	alignmentTest	=	models.BooleanField(default=False)
	flaws		    =   models.TextField(null=True,blank=True)
	extraInfo	    =   models.TextField("Additional Information",null=True,blank=True)
	contact			=	models.CharField(max_length=30)
	hideContact		=	models.BooleanField(default=False)
	financing		=	models.BooleanField(default=False)
	serviceContract	=	models.BooleanField(default=False)
	indexImage		=	models.ImageField(upload_to ='uploads/index_images/' ,null=True)
	termsAndConditionsAccepted= models.BooleanField(default=False)
	views			=	models.IntegerField(default=1)
	enlisted_days   =  models.IntegerField(default=1)
	date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)
	approve			=	models.BooleanField(default=False,blank=True,null=True)
	sold			=	models.BooleanField(default=False)

	def __str__(self):
		return self.model

#photos of cars
class CarImage(models.Model):
	image 			=	models.ImageField(upload_to ='uploads/listing_images/')
	car				=	models.ForeignKey(Car, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.car.title

#repair photos of car
class RepairedCarImage(models.Model):
	image 			=	models.ImageField(upload_to ='uploads/repair_images/')
	car				=	models.ForeignKey(Car, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.car.title


# Users' watchlist
class Watchlist(models.Model):
	user			=	models.ForeignKey(User,on_delete=models.CASCADE)
	car 			=	models.ForeignKey(Car,on_delete=models.CASCADE)
	# date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.user.email




# Direct messages
class Message(models.Model):
	sender= models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
	receiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="receiver")
	message=models.TextField()
	date=models.DateTimeField(auto_now_add=True, auto_now=False)
	readStatus=models.BooleanField(default=False)

	def __str__(self):
		return self.message


class UserStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    def last_seen(self):
        return cache.get('last_seen_%s' % self.user.username)
    
    def online(self):
        if self.last_seen():
            now = datetime.datetime.now()
            if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
                return False
            else:
                return True
        else: 
            return False


# Users' Comments
class Comment(models.Model):
	car	=	models.ForeignKey(Car,on_delete=models.CASCADE,related_name='comments')
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	content=	models.TextField()
	reply = models.ForeignKey('Comment',on_delete=models.CASCADE, null=True , blank=True, related_name="replies")
	#email = models.EmailField()
	date 			=	models.DateTimeField(auto_now_add=True, auto_now=False)
	readStatus		=	models.BooleanField(default=False)

	class Meta:
    		ordering =['date']
