from django.contrib import admin
from .models import item,Menu,User

class iteminline(admin.TabularInline):
    model=item
class MenuAdmin(admin.ModelAdmin):
    inlines = [iteminline, ]

admin.site.register(item)
#admin.site.register(item_menu)
admin.site.register(Menu)
admin.site.register(User)

# Register your models here.
