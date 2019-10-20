from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(category)
admin.site.register(sub_category)
admin.site.register(sub_child)
admin.site.register(sub_daughter)
admin.site.register(products)
admin.site.register(registered_as)
admin.site.register(customers)
admin.site.register(cart_items)
admin.site.register(orders)
admin.site.register(payments)
admin.site.register(shops)
admin.site.register(shopkpr)
admin.site.register(otd)
admin.site.register(customer_address)
