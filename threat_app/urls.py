from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views
from .views import RequestListCreateView

urlpatterns = [
    path('signup/', views.user_signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.process_request, name='dashboard'),  # Dashboard
    path('requests/', views.RequestListView.as_view(), name='request_list'),
    path('explore/', views.explore, name='explore'),
    path('about/', views.about, name='about'),
    path('requests/create/', views.RequestCreateView.as_view(), name='request_create'),
    path('requests/update/<int:pk>/', views.RequestUpdateView.as_view(), name='request_update'),
    path('requests/delete/<int:pk>/', views.RequestDeleteView.as_view(), name='request_delete'),
    path('api/requests/', RequestListCreateView.as_view(), name='api_requests'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
