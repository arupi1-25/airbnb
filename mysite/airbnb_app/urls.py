from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from .views import (UserProfileListAPIView,UserProfileDetailAPIView,CityViewSet,ReviewView,BookingViewSet,PropertyListAPIView,
                    PropertyDetailAPIView, RulesViewSet,ReviewEditView, PropertyCreateView, UserLoginView, UserRegisterView, LogoutView)
router = DefaultRouter()
router.register(r'city',CityViewSet, basename='city')
router.register(r'booking',BookingViewSet, basename='booking')
router.register(r'rules', RulesViewSet, basename='rules')
urlpatterns = [
    path('', include(router.urls)),
    path('property/', PropertyListAPIView.as_view(), name='property_list'),
    path('property/<int:pk>/', PropertyDetailAPIView.as_view(), name='property_detail'),
    path('property_create', PropertyCreateView.as_view(), name='property_generate'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('review/', ReviewView.as_view(), name='create_review'),
    path('review/<int:pk>/', ReviewEditView.as_view(), name='edit_review'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout')
]
