from django.urls import path, include
from rest_framework.routers import DefaultRouter
from restaurant import views


router = DefaultRouter()
router.register(r'categories', views.MenuCategoriesViewSet, basename="api_categories")
router.register(r'subcategoties', views.MenuSubCategoriesViewSet, basename="api_subcategories")
router.register(r'items', views.ItemsViewSet, basename="api_items")
router.register(r'tables', views.TablesViewSet, basename="api_tables")
router.register(r'orders', views.OrdersViewSet, basename="api_orders")
router.register(r'orderdetails', views.OrderDetailsViewSet, basename="api_orderdetails")
router.register(r'coupons', views.CouponViewSet, basename="api_coupons")


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('orderdetails/', views.OrderDetailsListView.as_view()),
]
