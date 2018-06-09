from django.contrib import admin

# Register your models here.
from .models import Airplane, Flight, Passanger, Ticket, CrewMember, Crew

admin.site.register(Airplane)
admin.site.register(Flight)
admin.site.register(Passanger)
admin.site.register(Ticket)
admin.site.register(Crew)
admin.site.register(CrewMember)