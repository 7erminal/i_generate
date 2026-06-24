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
    # path('api/videos/', views.VideoUploadView.as_view({'get': 'list', 'post': 'create'}), name='video-list'),
    # path('api/languages/', views.LanguageViewSet.as_view({'get': 'list', 'post': 'create'}), name='language-list'),
    # path('api/categories/', views.CategoryViewSet.as_view({'get': 'list', 'post': 'create'}), name='category-list'),
# 
]