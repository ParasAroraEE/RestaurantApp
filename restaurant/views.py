# django imports
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.conf import settings

from django.http.response import JsonResponse  # new
from django.views.decorators.csrf import csrf_exempt  # new


# python imports
import stripe

# app models import
from restaurant.models import MenuCategories, MenuSubCategories, Items, Tables, Orders, OrderDetails, Coupon, CustomerPayments

# app serializers import
from restaurant.serializers import ItemsSerializer, MenuSubCategoriesSerializer, MenuCategoriesSerializer, TablesSerializer, OrdersSerializer, OrderDetailsSerializer, CouponSerializer, CustomerPaymentsSerializer, RegistrationSerializer

# drf imports
from rest_framework import viewsets, filters, response, parsers, renderers, status
from rest_framework import generics
from rest_framework.response import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

stripe.api_key = settings.STRIPE_SECRET_KEY


@api_view(['POST', ])
def registration_view(request):

    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = "successfully registered a new user."
            data['email'] = account.email
            data['username'] = account.username
            token = Token.objects.get(user=account).key
            data['token'] = token
        else:
            data = serializer.errors
        return Response(data)


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


class CustomerPaymentsViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """

    serializer_class = CustomerPaymentsSerializer

    def get_queryset(self):

        try:
            return CustomerPayments.objects.all()
        except Exception as err:
            return {}


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    if request.method == 'POST':
        charge = stripe.Charge.create(
            amount=100,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        context = {
            'order': Orders.objects.get(id=2),
            'customer': Customers.objects.get(id=2),
            'bill': 100,
            'payment_id': charge['id'],
            'payment_amount': charge['amount_captured'],
            'payment_status': charge['status'],
            'payment_method': charge['payment_method'],
            'status': 1,
        }
        appointment = CustomerPayments.objects.create(**context)
        return render(request, 'charge.html', context)
