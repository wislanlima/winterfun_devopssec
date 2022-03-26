from django.contrib import admin

# Register your models here.
from .models import Profile, Relationship


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "gender", "country", "city"]
    list_filter = ["gender", "country", "city"]
    list_display_links = ["id", "user"]


admin.site.register(Profile, ProfileAdmin)

admin.site.register(Relationship)
