from django.contrib import admin
from . models import Car,CarImages
# Register your models here.
class CarAdmin(admin.ModelAdmin):
    #list_display=['device','value','timestamp']
    search_fields=['vin','model']

    class Meta:
        model= Car

admin.site.register(Car,CarAdmin)
admin.site.register(CarImages)