from django.contrib import admin


from django.utils.safestring import mark_safe

from restaurant.models import MenuCategories, MenuSubCategories, Items, Tables, Orders, OrderDetails, Coupon
from django.contrib.auth.models import User, Group


# admin.site.site_header = 'Restaurant'
# admin.site.site_title = 'Restaurant'
# admin.site.site_url = 'https://www.panel.chefforallseasons.co.uk/admin'
admin.site.index_title = 'Restaurant'
admin.empty_value_display = '**Empty**'


admin.site.unregister(Group)


class MenuCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img', 'status', 'featured')
    list_display_links = ("name",)
    search_fields = ("name", "id")
    list_filter = ("name", "status", "featured")
    fields = (('name',), 'image', ('status', 'featured'), 'Categories_image')
    icon_name = 'apps'
    readonly_fields = ["Categories_image"]
    # fieldsets = [
    #     (None, {'fields': ['id', 'name', 'image']}),
    #     ('Advance information', {'fields': ['status', 'featured', 'created_at', 'updated_at'], 'classes':['collapse']}),
    # ]

    def Categories_image(self, obj):
        return mark_safe('<img src="{url}" width="300px" height="300px" />'.format(url=obj.image.url,))

    def img(self, obj):
        return mark_safe('<img src="{url}",  width="50px" height="50px" />'.format(url=obj.image.url))


admin.site.register(MenuCategories, MenuCategoriesAdmin)


class MenuSubCategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'img', 'cateory', 'status', 'featured')
    list_display_links = ("name",)
    search_fields = ("name", "id")
    list_filter = ("name", "status", "featured", "cateory")
    fields = (('name', 'cateory'), 'image', ('status', 'featured'), 'Sub_Categories_image')
    icon_name = 'view_list'
    readonly_fields = ["Sub_Categories_image"]

    def Sub_Categories_image(self, obj):
        return mark_safe('<img src="{url}" width="300px" height="300px" />'.format(url=obj.image.url,))

    def img(self, obj):
        return mark_safe('<img src="{url}",  width="50px" height="50px" />'.format(url=obj.image.url))


admin.site.register(MenuSubCategories, MenuSubCategoriesAdmin)


class ItemsAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'img', 'sub_cateory', 'status', 'featured')
    list_display_links = ("name",)
    search_fields = ("name", "sub_cateory")
    list_filter = ("name", "status", "featured", "sub_cateory")
    fields = (('sub_cateory', 'name', 'price'), 'image', ('status', 'featured'), 'item_image')
    icon_name = 'local_dining'
    readonly_fields = ["item_image"]

    def item_image(self, obj):
        return mark_safe('<img src="{url}" width="300px" height="300px" />'.format(url=obj.image.url,))

    def img(self, obj):
        return mark_safe('<img src="{url}",  width="50px" height="50px" />'.format(url=obj.image.url))


admin.site.register(Items, ItemsAdmin)


class TablesAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'seating', 'img', 'status', 'featured')
    list_display_links = ("table",)
    search_fields = ("table", "id", "seating")
    list_filter = ("table", "status", "featured", "seating")
    fields = (('table', 'seating'), 'image', ('status', 'featured'), 'table_image')
    icon_name = 'airline_seat_recline_extra'
    readonly_fields = ["table_image"]

    def table_image(self, obj):
        return mark_safe('<img src="{url}" width="300px" height="300px" />'.format(url=obj.image.url,))

    def img(self, obj):
        return mark_safe('<img src="{url}",  width="50px" height="50px" />'.format(url=obj.image.url))


admin.site.register(Tables, TablesAdmin)


class OrderDetailsInline(admin.TabularInline):
    model = OrderDetails
    extra = 1

    classes = ("grp-collapse grp-open",)
    fieldsets = (
        ("", {
            "fields": ("item", "food_qty", "item_price",),
        }),
    )


class OrdersAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_number', 'table_number', 'date', 'bill_amount', 'payment_status', 'order_status')
    list_display_links = ("order_number",)
    search_fields = ("order_number", "id", "date", "payment_status", "order_status")
    list_filter = ("order_number", "id", "date", "payment_status", "order_status")
    fields = (('order_number', 'table_number', 'date'), ('bill_amount', 'discount_bill_amount'), ('coupon', 'discount'), ('payment_status', 'order_status'))
    icon_name='assignment'
    inlines=[OrderDetailsInline]


admin.site.register(Orders, OrdersAdmin)


class OrderDetailsAdmin(admin.ModelAdmin):
    list_display=('id', 'order_number')
    list_display_links=("id",)
    search_fields=("order_number",)
    list_filter=("order_number",)
    fields=(('order_number',), ('item', 'food_qty', 'item_price'))
    icon_name='add_shopping_cart'
    # inlines = [OrderDetailsInline]

    # fieldsets = [
    #     (None, {'fields': ['id', 'order_number', 'table_number']}),
    #     ('Order Detail', {'fields': ['item', 'food_qty', 'item_price']}),
    # ]


admin.site.register(OrderDetails, OrderDetailsAdmin)


class CouponDetailsAdmin(admin.ModelAdmin):
    list_display=('code', 'discount_type', 'discount_value', 'valid_from', 'valid_till', 'status')
    list_display_links=("code",)
    search_fields=("order_number", "discount_value")
    list_filter=("status", "discount_type")
    fields=(('code',), ('discount_type', 'discount_value'), ('valid_from', 'valid_till', 'status'), 'description')
    icon_name='payment'


admin.site.register(Coupon, CouponDetailsAdmin)
