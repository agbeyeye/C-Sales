from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from django.urls import reverse  
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.core.mail import send_mail,BadHeaderError
from rebuiltExotics.settings import DEFAULT_FROM_EMAIL,DEFAULT_TO_EMAIL
from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from .forms import CreateRegistrationForm, ImageForm,PasswordResetForm, UserProfileForm,CommentForm
from django.contrib.auth.decorators import login_required
# from django.contrib.gis.utils import GeoIP
from .models import Car, CarImage, RepairedCarImage, Comment, Message, Watchlist,UserProfile
from django.views.decorators.csrf import csrf_exempt
from django.db.models.signals import post_save
from django.dispatch import receiver
import time
UserModel=get_user_model()



# Create your views here
def homePage(request):
    context={}
    template='home.html'
    if request.user.is_authenticated:
        # get profile picture
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context['photo']=profile.photo.url

    try:
        popular_vehicles = get_popular_listing(3)
        recent_vehicles = get_recently_added_listing(3)
        context['popular_vehicles']=popular_vehicles
        context['recent_vehicles']=recent_vehicles
        print('list of  recent vehicles',recent_vehicles)
       
        # g = GeoIP()
        # ip = request.META.get('REMOTE_ADDR', None)
        # if ip:
        #     city = g.city(ip)['city']
        #     print(city)
        
        return render(request, template,context)
    except:
        if request.user.is_authenticated:
            return render(request, template,context)
        else:
            return render(request, template)


# login
@csrf_exempt
def loginUser(request):
    # POST request
    if request.POST and request.is_ajax():
        username = request.POST.get('username')
        password = request.POST.get('password')
        # print(username, password)
        # authenticate user
        try:
            user = authenticate(request, username=username, password=password)
            # if user is valid
            if user is not None:
                # login user
                login(request, user)
                print('login successful')
                response_data={'success':True}
            else:
                response_data={'success':False}
            return JsonResponse(response_data)
        except:
            response_data={'success':False}
            return JsonResponse(response_data)
    template = 'home.html'
    return render(request, template)


# logout user
def logoutUser(request):
    logout(request)
    return redirect('home')


# create new user account 
def registerPage(request):
    form = CreateRegistrationForm
    profileForm =UserProfileForm
    print('view accessed')
    if request.method == 'POST':
        print('post accessed')
        form = CreateRegistrationForm(data=request.POST)
        profileForm = request.FILES.getlist('photo')
        print(form.errors)
        print(profileForm)
        if form.is_valid() and profileForm:
            form.save()
            print('form is saved')
            messages.success(request, 'Account created successfully')
            print('account created successfully')
            user =User.objects.get(username=request.POST['username'])
            if user:
                # save user profile photo
                profile = UserProfile(user = user, photo= profileForm[0])
                profile.save()
                print('saved profile photo successfuly')
                # send verification mail to user
                try:
                    current_site = get_current_site(request)
                    mail_subject = 'Activate your account'
                    message = loader.render_to_string('account_activate.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    receipent_email = form.cleaned_data.get('email')
                    send_mail(subject=mail_subject,message=message,from_email=DEFAULT_FROM_EMAIL,recipient_list=[receipent_email])
                    print('Email confirmation message was sent successfully')
                except BadHeaderError:
                    return HttpResponse('Invalid header found!') 

            return redirect('home')
            
            
    context = {'form': form, 'imgForm':profileForm}
    template = "register.html"
    return render(request, template, context)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        template ='email-confirmation-done.html'
        return render(request,template)
    else:
        return HttpResponse('Activation link is invalid!')

def forgetPassword(request):
    '''
    This method implements the working logic of the forget password page.
    '''
    if request.method=='POST':
        email =request.POST['email']
        user =User.objects.get(email=email)
        print(user.email)
        if user is not None:
            try:
                content ={
                'email': user.email,
                            'domain': request.META['HTTP_HOST'],
                            'site_name': 'Rebuilt Exotics',
                            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                            'user': user,
                            'token': default_token_generator.make_token(user),
                            'protocol': 'http',
                             } 
                subject_template_name='reset_subject.txt'
                email_template_name='passwordresetemail.html' 
                subject = loader.render_to_string(subject_template_name, content)
                subject = ''.join(subject.splitlines())
                email = loader.render_to_string(email_template_name, content)
                send_mail(subject, email, DEFAULT_FROM_EMAIL , [user.email], fail_silently=False) 
                return redirect(reverse('reset-password-done'))
            except BadHeaderError:
                return HttpResponse('Invalid header found!') 

    else:
        x = messages.error(request, 'This email does not exist in the system. Enter a valid email') 
        template ='forgetpassword.html'
        return render(request,template ) 
    template='forgetpassword.html'    
    return render(request,template,{})  


def resetpassword_confirm(response, uidb64=None, token=None, *arg, **kwargs):
    '''
    This function implements the user reset password route
    '''
    form =PasswordResetForm
    if response.method =='POST':
        form=PasswordResetForm(data=response.POST)
        print(form.errors)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']

            UserModel = get_user_model()
            assert uidb64 is not None and token is not None 
            try:
                    uid = urlsafe_base64_decode(uidb64)
                    user = UserModel._default_manager.get(pk=uid)
                    
            except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return redirect(reverse('reset-password-complete'))
                else:
                    return redirect(reverse('reset-fail'))  
            else:
                return redirect(reverse('reset-fail')) 
    context = {'form': form}            
    template='passwordresetconfirm.html'     
    return render(response,template,context)
               

def passwordresetdone(request):
    template ='passwordresetdone.html'
    
    return render(request,template) 
def passwordresetconfirm(response):
   
    template ='passwordresetconfirm.html'
    return render(response,template) 


def invalidReset(response):
    template ='passwordresetinvalid.html'
    return render(response,template) 

def passwordresetcomplete(response):
    template='password-reset-complete.html'
    return render(response,template)


# request for vehicle submission

def submit_car(request):
    template = 'submit-car.html'
    if request.user.is_authenticated:
        # get profile photo of user
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context = {'photo':profile.photo.url}
            return render(request, template,context)
    return render(request, template)

#about page request
def about(request):
    template = 'about.html'
    if request.user.is_authenticated:
        # get profile photo of user
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context = {'photo':profile.photo.url}
            return render(request, template,context)
    return render(request, template)


#request for sold vehicles
def sold_vehicles(request):
    template='sold-vehicle.html'
    sold_vehicles = list(Car.objects.filter(sold=True).values())
    if sold_vehicles:
        context={'vehicles':sold_vehicles}
        return render(request,template,context)
    return render(request,template)


# car detail for listing endpoint
# def submit_car_detail(request):
#     if request.method == 'POST':
#         form = request.POST
#         print("form here",form)
#         return redirect('home')
#     template = 'car-detail.html'
#     return render(request, template)


# get list of vehicles
def vehicle_list(request,sortBy):
    template = 'vehicle-list.html'
    vehicles = sort_listings_by(sortBy)
    if vehicles:
        return render(request,template,{'vehicles':vehicles})
    return render(request, template)

# get list of popular vehicles
def popular_vehicles(request):
    context={}
    template = 'vehicle-list.html'
    vehicles = sort_listings_by("popular")
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context['photo']=profile.photo.url
    if vehicles:
        context['vehicles']=vehicles
        return render(request,template,context)
    return render(request, template)

#get list of recent vehicles
def recent_vehicles(request):
    context={}
    template = 'vehicle-list.html'
    vehicles = sort_listings_by("recent")
    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context['photo']=profile.photo.url
    if vehicles:
        context['vehicles']=vehicles
        return render(request,template,context)
    return render(request, template)
# get a single vehicle data
def vehicle_detail(request,vehicle_id):
    template ='vehicle.html'
    new_comment =None  
    car=get_object_or_404(Car,pk=vehicle_id)  
    comments =car.comments.filter(readStatus=True)
    if request.method =='POST':
        form =CommentForm(data=request.POST or None)
        if form.is_valid():
            content = request.POST.get('content')
            reply_id = request.POST.get('parent_id')             
            comment_qs=None 
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
            comment = Comment.objects.create(car=car, user=request.user, content=content, reply=comment_qs)             
            comment.save()
            #print('The primary key of the new comment',new_comment.pk)
            vehicle = Car.objects.get(id=vehicle_id)
            print('Vehicle ----',vehicle.seller)
            user =User.objects.get(username =vehicle.seller)
            print('user email---',user.email)
            # seller=vehicle.objects.get(seller=request.user)
            # print('Seller --users', seller)
            comment_id=Comment.objects.get(pk=comment.pk)
            print(comment_id)
            if user:
                try:
                    current_site = get_current_site(request)
                    mail_subject = 'Approve User comment'
                    message = loader.render_to_string('approve_comment.html', {
                        'user':user,
                        'commentSender':request.user,
                        'content':request.POST['content'],
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                        'vehicle_id':vehicle_id,
                        'comment_id':comment.pk,
                    })
                    receipent_email = user.email
                    send_mail(subject=mail_subject,message=message,from_email=DEFAULT_FROM_EMAIL,recipient_list=[receipent_email])
                    print('Comment approval was was sent successfully')
                    return redirect(reverse('vehicle', kwargs={'vehicle_id':vehicle_id}))
                except BadHeaderError:
                    return HttpResponse('Invalid header found!')                   
      
    comment_form=CommentForm() 
    context={'car':car,'comment_form':comment_form,'new_comment':new_comment,'comments':comments}
    # template ='vehicle.html'
    # vehicle_id = vehicle_id
    vehicle = Car.objects.get(id=vehicle_id)
    vehicle_img = list(vehicle.carimage_set.all()[:3])
    context['vehicle_images']=vehicle_img
    context['vehicle']=vehicle   
    vehicle_id = vehicle_id
    vehicle = Car.objects.get(id=vehicle_id)
    # increase number of vehicle view
    vehicle.views = vehicle.views+1
    vehicle.save()
    # split video links and vehicle flaws into list
    if vehicle.videoLinks:
        links =  vehicle.videoLinks.split(',')
        for i in range(0,len(links)):
            links[i]= links[i].replace("watch?v=","embed/")
        context['video_links']=links
        print('links',links)
    if vehicle.flaws:
        flaws =  vehicle.flaws.split(',')
        context['flaws']=flaws
    if vehicle.upgrade:
        upgrade =  vehicle.upgrade.split(',')
        context['upgrade']=upgrade
    if vehicle.recentService:
        service =  vehicle.recentService.split(',')
        context['service']=service
    if vehicle.repair:
        repair =  vehicle.repair.split(',')
        context['repair']=repair
    # get vehicle images
    vehicle_img = list(vehicle.carimage_set.all()[:3])
    context['vehicle_images']=vehicle_img
    context['vehicle']=vehicle
    # get seller profile  photo
    seller =  vehicle.seller
    profile = UserProfile.objects.get(user=seller)
    context['profile_photo']=profile.photo.url
    if request.user.is_authenticated:
        # get profile picture
        profile = UserProfile.objects.get(user=request.user)
        if profile:
            context['photo']=profile.photo.url
            return render(request, template,context)
    return render(request,template,context)

    

def approve(request, uidb64, token,vehicle_id,comment_id):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        car=get_object_or_404(Car,pk=vehicle_id)
        comment =car.comments.get(id=comment_id) 
        comment.readStatus = True
        comment.save()
        template ='comment-approval-done.html'
        return render(request,template)
    else:
        return HttpResponse('Approval link was invalid!')


#request for vehicle images
def vehicle_images(request,vehicle_id):
    context={}
    template='show-car-pictures.html'
    vehicle_id = vehicle_id
    print('id',vehicle_id)
    vehicle = Car.objects.get(id=vehicle_id)
    images = list(vehicle.carimage_set.all())
    context['vehicle_images']=images
    context['image_count']=len(images)
    return render(request, template,context)


# Get listed cars
def get_all_listed_cars():
    enlisted_cars = Car.objects.filter(sold=False, enlisted_days__lte=120).values_list('views')
    return enlisted_cars

def car_pictures(request):
    template ='show-car-pictures.html'
    return render(request,template)

def contact_us(request):
    if request.method =='POST':
        full_name =request.POST['fullname']
        email=request.POST['email']
        print('User email :',email)
        subject='Message from '+full_name
        message=request.POST['message']+'\n Reply to the message using this email '+email
        try:
            message=EmailMessage(subject=subject,body=message,from_email=email,to=[DEFAULT_TO_EMAIL])
            message.send()
        except BadHeaderError:
            return HttpResponse('Invalid header found!') 
        return redirect('success')       

    template ='contact.html'
    return render(request,template)

def success(request):
    return HttpResponse('Success! Thank you for your message.')


# add new listing

@csrf_exempt
def submit_car_detail(request):
    if request.method == 'POST' and request.is_ajax():
        # get form data from Post request
        form_values = request.POST
        imageFiles = request.FILES.getlist('file')
        print('data',form_values)
        print('files',imageFiles)
        # set financing field to boolean
        finance = "Yes" in form_values.get('financing')
        # extract the fuel type from form data
        if form_values.get('fuel_type')=='other':
            global fuel_type
            fuel_type = form_values.get('other_fuel_type')
        else:
            fuel_type = form_values.get('fuel_type')

        # if user is authenticated
        if request.user.is_authenticated:
            # if form and files exist
            if form_values and imageFiles:
                # create new listing object
                new_car = Car(seller=request.user, sellerType=form_values['seller'],name=form_values.get('name'),
                              make=form_values['make'],
                              model=form_values['model'], Year=form_values['year'], trim=form_values['trim'],
                              engine=form_values['engine'], transmission=form_values['transmission'],
                              drivetrain=form_values['drive_train'], fuelType=fuel_type,
                              askingPrice=form_values['asking_price'], priceNegotiation=bool(form_values['price_negotiation']),
                              vin=form_values['vin'], title=form_values['title'], milleage=form_values['mileage'],
                              exteriorColor=form_values['exterior_color'],
                              interiorColor=form_values['interior_color'], wheelAlignment=form_values['wheel_alignment'],
                              country=form_values['country'],
                              state=form_values['state'],city=form_values['city'], zipCode=form_values['code'], upgrade=form_values['upgrade'],
                              repair=form_values['repair'],videoLinks = form_values.get('video_link'),
                              rebuildingLink=form_values['rebuilding_link'], recentService=form_values['recent_service'],
                              flaws=form_values.get('flaws'), extraInfo=form_values.get('extra_info'),
                              contact=form_values.get('contact'), hideContact=bool(form_values['hide_contact']),
                              financing=finance, serviceContract= bool(form_values['service_contract']),
                              termsAndConditionsAccepted=bool(form_values['terms_service']), indexImage =imageFiles[0])
                print('about to save')
                new_car.save()
                for item in imageFiles:
                    car_image = CarImage(car = new_car, image=item)
                    car_image.save()
                print('save car and images')
                response ={'success':True}
                return JsonResponse(response)
            else:
                response={'success':False}
                return JsonResponse(response)
    template = 'car-detail.html'
    if request.user.is_authenticated:
        # get profile picture
        profile = UserProfile.objects.get(user=request.user)
        print('photo',profile.photo.url)
        if profile:
            context = {'photo':profile.photo.url}
            return render(request, template,context)

    return render(request,template)


# Listings request by seller
@login_required
def my_listings(request):
    template='my-listing.html'
    seller = request.user
    # get listings
    listings = get_listed_cars_by_user(seller)
    context={'listings':listings}
    # get profile picture
    profile = UserProfile.objects.get(user=request.user)
    if profile:
        context['photo']=profile.photo.url

    return render(request,template,context)

# limited popular listing
def get_popular_listing(limit):
    vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('-views').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','indexImage')[:limit])

    return vehicles
    
# all popular listing
def get_popular_listing_all():
    vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('-views').values('id','make','model','Year','askingPrice','indexImage','engine','transmission','city','zipCode','drivetrain','milleage','vin'))
    return vehicles

# top recently added listing
def get_recently_added_listing(limit):
    vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('date').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','indexImage')[:limit])
    return vehicles

# all recently added
def get_recently_added_listing_all():
    vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('date').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    return vehicles


# get listings by seller
def get_listed_cars_by_user(seller):
    listings = list(Car.objects.filter(seller = seller).values())
    return listings

def sort_listings_by(param):
    vehicle=[]
    if param=="popular":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('-views').values('id','make','model','Year','askingPrice','indexImage','engine','transmission','city','zipCode','drivetrain','milleage','vin'))
    elif param =="recent":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('date').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param=="newest-year":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('-Year').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param=="oldest-year":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('Year').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param=="highest-price":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('-askingPrice').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param=="lowest-price":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('askingPrice').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param =="nearest":
        request_loc=''
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120,city=request_loc).order_by('-views').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))
    elif param=="all":
        vehicles = list(Car.objects.filter(approve=True,sold=False,enlisted_days__lte=120).order_by('date').values('id','make','model','Year','askingPrice','engine','transmission','city','zipCode','drivetrain','indexImage','milleage','vin'))

    return vehicles





# update listing
def update_listing(request):
    pass


# get single listing
def get_single_listing(request):
    id = request['id']
    car = Car.objects.get(Id=id)
    return car


# view watchlist
def get_watch_list(request):
    pass


# sell listing
def sell_listing(request):
    pass


# write message to a seller
def write_message(request):
    pass


# read message from a buyer
def read_message(request):
    pass


# pass comment/report/suggestion
def write_comment(request):
    pass


# reead comment
def read_comment(request):
    pass
