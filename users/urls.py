from django.urls import path
from .views import LoginView, UserView,NewestUserView,UserUpdateView,UserManagementView

urlpatterns = [
    path('accounts/',UserView.as_view() ),
    path('login/',LoginView.as_view() ),
    path('accounts/newest/<int:num>/',NewestUserView.as_view() ),
    path('accounts/<pk>/',UserUpdateView.as_view() ),
    path('accounts/<pk>/management/',UserManagementView.as_view() ),
]