# django imports
from django.shortcuts import render

# app models import
from restaurant.models import MenuCategories, MenuSubCategories, Items, Tables, Orders, OrderDetails, Coupon

# app serializers import
from restaurant.serializers import ItemsSerializer, MenuSubCategoriesSerializer, MenuCategoriesSerializer, TablesSerializer, OrdersSerializer, OrderDetailsSerializer, CouponSerializer

# drf imports
from rest_framework import viewsets, filters, response, parsers, renderers, status
from rest_framework import generics
from rest_framework.response import Response


class MenuCategoriesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = MenuCategoriesSerializer

    def get_queryset(self):

        try:
            return MenuCategories.objects.all()
        except Exception as err:
            return {}


class MenuSubCategoriesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = MenuSubCategoriesSerializer

    def get_queryset(self):

        try:
            return MenuSubCategories.objects.all()
        except Exception as err:
            return {}


class ItemsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = ItemsSerializer

    def get_queryset(self):

        try:
            return Items.objects.all()
        except Exception as err:
            return {}


class TablesViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = TablesSerializer

    def get_queryset(self):

        try:
            return Tables.objects.all()
        except Exception as err:
            return {}


class OrdersViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = OrdersSerializer

    def get_queryset(self):

        try:
            return Orders.objects.all()
        except Exception as err:
            return {}


class OrderDetailsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = OrderDetailsSerializer

    def get_queryset(self):

        try:
            return OrderDetails.objects.all()
        except Exception as err:
            return {}


class CouponViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = CouponSerializer

    def get_queryset(self):

        try:
            return Coupon.objects.all()
        except Exception as err:
            return {}

# class OrderDetailsListView(generics.ListAPIView):

#     serializer_class = OrderDetailsSerializer

#     def get_queryset(self):
#         return OrderDetails.objects.all()

#     def list(self, request, *args, **kwargs):

#         res = super(OrderDetailsListView, self).list(request, *args, **kwargs)
#         datas = res.data
#         print(datas)
#         case_list = []
#         for k, v in enumerate(datas):

#             case = {
#                 "OrderNumber": datas[k]['order_number_number'],
#                 "Item": datas[k]['item_name'],
#                 "Qty": datas[k]['food_qty'],
#                 "Price": datas[k]['item_price_value'],
#                 "Price": datas[k]['item_price_value'] * datas[k]['food_qty']
#             }
#             case_list.append(case)
#         if len(case_list) > 0:
#             res.data = {"message": "Attributes retrieve successfully", "status": 200, "response": case_list}
#         else:
#             res.data = {"message": "No data found"}

#         return res
