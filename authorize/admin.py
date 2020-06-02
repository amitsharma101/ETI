from django.contrib import admin
from .models import extendeduser,ProfileFields,FieldValues,VerificationRequests

# Register your models here.
admin.site.register(extendeduser)
admin.site.register(ProfileFields)
admin.site.register(FieldValues)
admin.site.register(VerificationRequests)