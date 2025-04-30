from django.contrib import admin
from .models import Service, Specialist, Appointment

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'duration')
    list_editable = ('name', 'duration')

@admin.register(Specialist)
class SpecialistAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id')
    filter_horizontal = ('services',)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'specialist_id', 'service_id', 'start_time', 'status')
    list_filter = ('status', 'start_time')
    raw_id_fields = ('client', 'specialist', 'service')