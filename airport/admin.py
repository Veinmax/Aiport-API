from django.contrib import admin

from .models import (
    Airplane,
    AirplaneType,
    Crew,
    Airport,
    Route,
    Flight,
    Order,
    Ticket
)

admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Crew)
admin.site.register(Airport)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Order)
admin.site.register(Ticket)
