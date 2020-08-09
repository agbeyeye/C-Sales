from django.shortcuts import render,redirect
from django.http import HttpResponse
#from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import CreateRegistrationForm
from . models import Car, CarImages, RepairedCarImages, Comments,Messages,watchlist


# Create your views here
def homePage(request):
	return render(request,'home.html')




#login
def loginPage(request):

	#post request
	if request.method=='POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		#authenticate user
		user = authenticate(request, username=username, password=password)
		#if user is valid
		if user is not None:
			#login user
			login(request,user)
			return redirect('home')
		else:
			messages.info(request,'username or password is invalid')

	template= "login.html"
	return render(request,template)




#logout user
def logoutUser(request):

	logout(request)
	return redirect('home')




#create new user account
def registerPage(request):

	form = CreateRegistrationForm
	
	if request.method == "POST":
		form = CreateRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,'Account created successfully')
			return redirect('login')
	context = {'form':form}
	template= "register.html"
	return render(request,template,context)




#Get listed cars
def get_all_listed_cars():
	enlisted_cars = Car.objects.filter(sold=False,enlisted_days<121).values_list('views')
	return enlisted_cars



#add new listing
def add_new_listing(request):
	if request.method='POST':
		form_values = eval(bytes.decode(request.body))
		if request.user.is_authenticated:
			new_car = Car(seller = request.user, sellerType = form_values['sellerType'], Id='createUniqueId', make = form_values['make'],
				model=form_values['model'],Year=form_values['year'],trim=form_values['trim'], engine =form_values['engine'], transmission=form_values['transmission'],
				drivetrain=form_values['drivetrain'],fuelType=form_values['fuelType'],askingPrice=form_values['askingPrice'],priceNegotiation=form_values['priceNegotiation'],
				vin=form_values['vin'],title =form_values['title'],milleage=form_values['milleage'],exteriorColor=form_values['exteriorColor'],
				interiorColor=form_values['interiorColor'],wheelAlignment=form_values['wheelAlignment'], country=form_values['country'],
				state=form_values['state'],zipCode=form_values['zipCode'],upgrade=form_values['upgrade'],repair=form_values['repair'],
				rebuildingLink=form_values['rebuildingLink'],recentService=form_values['recentService'],alignmentTest=form_values['alignmentTest'],
				flaws=form_values['flaws'],extraInfo=form_values['extraInfo'],contact=form_values['contact'],hideContact=form_values['hideContact'],
				financing=form_values['financing'],serviceContract=form_values['serviceContract'],termsAndConditionsAccepted=form_values['termsAndConditionsAccepted'])
			new_car.save()



#update listing
def update_listing(request):
	pass


#get single listing
def get_single_listing(request):
	id = request['id']
	car = Car.objects.get(Id=id) 
	return car



#view watchlist
def get_watch_list(request):
	pass



#sell listing
def sell_listing(request):
	pass



#write message to a seller
def write_message(request):
	pass



#read message from a buyer
def read_message(request):
	pass



#pass comment/report/suggestion
def write_comment(request):
	pass



#reead comment
def read_comment(request):
	pass
