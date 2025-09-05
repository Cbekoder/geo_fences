from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import GeoFence, DeviceState

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(GeoFence)
class GeoFenceAdmin(admin.ModelAdmin):
    list_display = ("name", "center_lat", "center_lon", "radius_km")


@admin.register(DeviceState)
class DeviceStateAdmin(admin.ModelAdmin):
    list_display = ("device_id", "is_inside", "updated_at")
    search_fields = ("device_id",)