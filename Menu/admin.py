from django.contrib import admin
from .models import item,item_menu,Menu,seat,table,order,order_item,payment

class itemInline(admin.TabularInline):
    model=item
    raw_id_fields=('menu_key',)
    extra =1


# class itemsecInline(admin.TabularInline):
#     model = item
# class select(admin.ChoicesFieldListFilter):
#     formfield_for_choice_field
class MenuAdmin(admin.ModelAdmin):
    inlines = [itemInline, ]
    #select
class seatInline(admin.TabularInline):
    model=seat
    raw_id_fields=('table_key',)
    extra =1
class tableAdmin(admin.ModelAdmin):
    inlines = [seatInline, ]

admin.site.register(item)
admin.site.register(item_menu)
#admin.site.register(Menu)
admin.site.register(Menu,MenuAdmin)
admin.site.register(table,tableAdmin)
admin.site.register(order)
admin.site.register(order_item)
admin.site.register(payment)