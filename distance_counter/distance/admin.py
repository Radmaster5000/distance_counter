from django.contrib import admin

from .models import Office, Person, Unit, Distance

# Register your models here.
admin.site.register(Office)
admin.site.register(Person)
admin.site.register(Unit)
admin.site.register(Distance)
