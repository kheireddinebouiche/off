from django.contrib import admin
from .models import Profile, Menu, Item, OrderItem, Order,ModeConso

# Register your models here.

admin.site.register(Profile),
admin.site.register(Menu),
admin.site.register(Item),
admin.site.register(OrderItem),
admin.site.register(Order),
admin.site.register(ModeConso),
