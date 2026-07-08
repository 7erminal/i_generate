from django.urls import include, path
from rest_framework import routers

from eezy_source import views

router = routers.DefaultRouter()
router.register(r'currencies', views.CurrencyViewSet, basename='currency')
router.register(r'unit', views.SystemUnitsViewSet, basename='unit')
router.register(r'configs', views.ConfigurationViewSet, basename='config')
router.register(r'fx', views.FXViewSet, basename='fx')
router.register(r'receipts', views.ReceiptViewSet, basename='receipt')

urlpatterns = [
    path('api/', include(router.urls)),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
# 
]