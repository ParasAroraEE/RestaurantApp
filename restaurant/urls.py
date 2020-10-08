from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views
from rest_framework.authtoken.views import obtain_auth_token

router = DefaultRouter()
router.register(r'categories', views.MenuCategoriesViewSet, basename="api_categories")
router.register(r'subcategoties', views.MenuSubCategoriesViewSet, basename="api_subcategories")
router.register(r'items', views.ItemsViewSet, basename="api_items")
router.register(r'tables', views.TablesViewSet, basename="api_tables")
router.register(r'orders', views.OrdersViewSet, basename="api_orders")
router.register(r'orderdetails', views.OrderDetailsViewSet, basename="api_orderdetails")
router.register(r'coupons', views.CouponViewSet, basename="api_coupons")
router.register(r'customerpayments', views.CustomerPaymentsViewSet, basename="api_customerpayments")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('home/', views.HomePageView.as_view(), name='home'),
    path('charge/', views.charge, name='charge'),
    # path('config/', views.stripe_config),  # new
    # path('create-checkout-session/', views.create_checkout_session),
    # path('success/', views.SuccessView.as_view()),  # new
    # path('cancelled/', views.CancelledView.as_view()),  # new
    # path('orderdetails/', views.OrderDetailsListView.as_view()),
    # path('test-payment/', views.test_payment),
    path('register/', views.registration_view, name='register'),
    path('login/', obtain_auth_token, name='login'),
]
