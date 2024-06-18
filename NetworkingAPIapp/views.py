from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

import datetime
import pytz

# IMPORTING SERVICE MODULES AND SERIALIZERS
from .serializer import CreateLoginSerializer, LoginSerializer
from.Services.Login import CreateUser, ReadLogin
from .Services.user_search_service import UserSearchService, FriendRequestService,\
                                          FriendsListService, PendingFriendRequestsService


ist = pytz.timezone('Asia/Kolkata')
now = datetime.datetime.now(ist)


class Create_User_Api(APIView):

    def post(self, request):
        serializer = CreateLoginSerializer(data=request.data)
        if serializer.is_valid():
            ob1 = CreateUser(serializer)
            return_data = ob1.start_process()
            if return_data['status'] == status.HTTP_200_OK:
                return Response(return_data['data'], return_data['status'])
            else:
                return Response(return_data['data'], status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class User_login_api(APIView):

    def get(self, request):
        data = request.GET
        serializer = LoginSerializer(data=data)

        if serializer.is_valid():
            ob1 = ReadLogin(serializer)
            return_data = ob1.start_process()
            if return_data['status'] == status.HTTP_200_OK:
                return Response(return_data['data'], return_data['status'])
            else:
                return Response(return_data['data'], status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# search api
class UserSearchView(APIView):
    def get(self, request):
        service = UserSearchService()
        return service.search_users(request)


class FriendRequestView(APIView):

    def post(self, request):
        from_user = request.data.get('from_user')
        to_user = request.data.get('to_user')

        if not from_user or not to_user:
            return Response({"detail": "Both from_user and to_user are required"}, status=status.HTTP_400_BAD_REQUEST)
        service = FriendRequestService()
        return service.send_friend_request(from_user, to_user)

    def put(self, request):
        from_user = request.data.get('from_user')
        to_user = request.data.get('to_user')
        action = request.data.get('action')

        service = FriendRequestService()
        return service.accept_reject_friend_request(from_user, to_user, action)


class FriendsListView(APIView):

    def get(self, request, user_email):
        service = FriendsListService()
        return service.list_friends(user_email)


class PendingFriendRequestsView(APIView):

    def get(self, request, user_email):
        service = PendingFriendRequestsService()
        return service.list_pending_requests(user_email)
