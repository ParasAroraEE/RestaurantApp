# drf imports
from rest_framework import serializers

# app model import
from restaurant.models import MenuCategories, MenuSubCategories, Items, Tables, Orders, OrderDetails, Coupon


class ItemsSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField(required=False)
    # sub_cateory_name = serializers.SerializerMethodField()

    class Meta:
        model = Items
        fields = ['name', 'price', 'image']
        # fields = ['id', 'name', 'price', 'image', 'sub_cateory', 'sub_cateory_name']

    # def get_sub_cateory_name(self, obj):
    #     if obj.sub_cateory:
    #         return obj.sub_cateory.name
    #     return ""

class MenuSubCategoriesSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField(required=False)
    items = ItemsSerializer(many=True, required=False)
    # cateory_name = serializers.SerializerMethodField()

    class Meta:
        model = MenuSubCategories
        fields = ['name', 'image', 'items']
        # fields = ['id', 'cateory', 'cateory_name', 'name', 'image', 'items']

    # def get_cateory_name(self, obj):
    #     if obj.cateory:
    #         return obj.cateory.name
    #     return ""

class MenuCategoriesSerializer(serializers.ModelSerializer):

    # id = serializers.IntegerField(required=False)
    subcategory = MenuSubCategoriesSerializer(many=True, required=False)

    class Meta:
        model = MenuCategories
        fields = ['name', 'image', 'subcategory']
        # fields = ['id', 'name', 'image', 'subcategory']


class TablesSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    table_status = serializers.SerializerMethodField()

    class Meta:
        model = Tables
        fields = ['table', 'seating', 'image', 'status', 'id', 'table_status']

    def get_table_status(self, obj):
        table_num = get_table_status(obj.id)
        # print(table_num)
        if obj.id:
            if obj.id in table_num:
                obj.status = 'Booked'
                obj.save()
            elif obj.id not in table_num:
                obj.status = 'Vacent'
                obj.save()
            return obj.status
        return ""


class CouponSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)

    class Meta:
        model = Coupon
        fields = ['code', 'discount_type', 'discount_value', 'valid_from', 'valid_till', 'status']


class OrderDetailsSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    order_number_number = serializers.SerializerMethodField()
    item_price = serializers.DecimalField(decimal_places=2, max_digits=10, required=False)
    item_name = serializers.SerializerMethodField()
    # item_price_value = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = OrderDetails
        fields = ['id', 'order_number', 'item', 'order_number_number', 'item_name', 'food_qty', 'item_price', 'total_amount']

    def get_order_number_number(self, obj):
        if obj.order_number:
            return obj.order_number.order_number
        return ""

    def get_item_name(self, obj):
        if obj.item:
            return obj.item.name
        return ""

    # def get_item_price_value(self, obj):
    #     if obj.item:
    #         return obj.item.price
    #     return ""

    def get_total_amount(self, obj):
        if obj.item and obj.food_qty:
            return obj.item.price * obj.food_qty
        return ""


class OrdersSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(required=False)
    table_number_number = serializers.SerializerMethodField()
    coupon_code = serializers.SerializerMethodField()
    orderdetails = OrderDetailsSerializer(many=True, required=False)

    class Meta:
        model = Orders
        fields = ['id', 'order_number', 'table_number_number', 'date', 'bill_amount', 'discount', 'discount_bill_amount', 'payment_status', 'order_status', 'orderdetails', 'coupon', 'coupon_code']

    def get_table_number_number(self, obj):
        if obj.table_number:
            # print(obj.table_number.status)

            return obj.table_number.table
        return ""

    def get_coupon_code(self, obj):
        if obj.coupon:
            data = {"code": obj.coupon.code, "type": obj.coupon.discount_type, "value": obj.coupon.discount_value}
            return data
        return ""


def get_table_status(table_number):

    table_status = Orders.objects.select_related('table_number').filter(payment_status='Pending')
    booked_tables = []
    for i in table_status:
        d = {
            "numbr": i.table_number.id,

        }
        booked_tables.append(d["numbr"])

    return booked_tables
