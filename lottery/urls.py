"""lottery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
from mainapp.views import GetUserTransactions, WithdrawPoints, BetStatusGame1, BetStatusGame2, NextResultTime, BetView, CreateManagerView, CreateBrokerView, SendPoints, CreateUserView, ListCreatedUsers, UserViewSet, CurrentUserDetails, ListBrokers, GetIncomingTransactions, GetOutgoingTransactions, GetAllTransactions, ListAllUsers
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.obtain_auth_token),
    path('create-broker/', CreateBrokerView.as_view()),
    path('create-manager/', CreateManagerView.as_view()),
    path('create-user/', CreateUserView.as_view()),
    path('list-created-users/', ListCreatedUsers.as_view()),
    path('list-all-users/', ListAllUsers.as_view()),
    path('user-details/<int:pk>',UserViewSet.as_view({'get': 'retrieve'})),
    path('account-details/',CurrentUserDetails.as_view()),
    path('broker-list/', ListBrokers.as_view()),
    path('send-points/', SendPoints.as_view()),
    path('incoming-transactions/', GetIncomingTransactions.as_view()),
    path('outgoing-transactions/', GetOutgoingTransactions.as_view()),
    path('bet/', BetView.as_view()),
    path('user-history/', GetAllTransactions.as_view()),
    path('game1-status/', BetStatusGame1.as_view()),
    path('game2-status/', BetStatusGame2.as_view()),
    path('withdraw-points/',WithdrawPoints.as_view()),
    path('next-result', NextResultTime.as_view()),
    path('user-transactions/<int:pk>', GetUserTransactions.as_view()),
    
]
