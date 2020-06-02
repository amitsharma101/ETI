from django.contrib import admin
from .models import extendeduser,ProfileFields,FieldValues

# Register your models here.
admin.site.register(extendeduser)
admin.site.register(ProfileFields)
admin.site.register(FieldValues)