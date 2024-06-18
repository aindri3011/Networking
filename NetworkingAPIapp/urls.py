from django.urls import path
from . import views

urlpatterns = [

    # USER CREATION
    path('create-user/', views.Create_User_Api.as_view()),
    # LOGIN USER TO PORTAL
    path('login-user/', views.User_login_api.as_view()),

    # FUNCTIONAL APIS ENDPOINTS
    path('search/', views.UserSearchView.as_view()),
    path('friend-request/', views.FriendRequestView.as_view(), name='friend-request'),
    path('friends/<str:user_email>/', views.FriendsListView.as_view(), name='friends-list'),
    path('pending-requests/<str:user_email>/', views.PendingFriendRequestsView.as_view(), name='pending-requests'),
]
