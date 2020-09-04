from django.contrib import admin
from . models import Car,CarImage,Comment,Watchlist,Message
# Register your models here.
class CarAdmin(admin.ModelAdmin):
    search_fields=['model','make','vin','engine','Year','transmission']
    list_display=['title','model','make','vin','engine','Year','transmission','milleage','enlisted_days','approve']
    list_filter=['approve','model','make','engine','Year','enlisted_days','sold','country','state','city']

    class Meta:
        model= Car

class CommentAdmin(admin.ModelAdmin):
    search_fields=['user']
    list_filter=['readStatus','date']
    list_display=['user','content','date','readStatus']

    class Meta:
        model = Comment

class MessageAdmin(admin.ModelAdmin):
    search_fields=['sender','receiver']
    list_filter=['date']
    list_display=['sender','receiver','message','date']

    class Meta:
        model = Message

admin.site.register(Car,CarAdmin)
admin.site.register(CarImage)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Message,MessageAdmin)

# site config
admin.site.site_header = "RebuiltExotics Admin Portal"
admin.site.site_title = "RebuiltExotics Admin"
admin.site.index_title = "RebuiltExotics"
