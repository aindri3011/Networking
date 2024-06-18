from collections import defaultdict
import datetime

import pytz
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from ..mongodb import user_collection, connect_collection
from ..serializer import UserSerializer, FriendRequestSerializer


class UserSearchService:

    """
    IMPLEMENTATION OF SEARCH QUERY TO SEARCH EXISTING USER
    """
    def __init__(self):
        self.users_collection = user_collection

    def search_users(self, request):
        keyword = request.query_params.get('keyword', '')
        if not keyword:
            return Response({"detail": "Keyword is required"}, status=status.HTTP_400_BAD_REQUEST)

        paginator = PageNumberPagination()
        paginator.page_size = 10  # EACH PAGE SHOWING 10 RECORDS PER PAGE

        query = {
            "$or": [
                {"email_id": {"$regex": keyword, "$options": 'i'}},
                {"name": {"$regex": keyword, "$options": 'i'}}
            ]
        }
        users = self.users_collection.find(query)
        result_page = paginator.paginate_queryset(list(users), request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FriendRequestService:
    """
    IMPLEMENTATION FOR MANAGING FRIEND REQUEST
    """

    request_count = defaultdict(list)

    def __init__(self):
        self.users_collection = user_collection
        self.friend_requests_collection = connect_collection

    def send_friend_request(self, from_user, to_user):
        ist = pytz.timezone('Asia/Kolkata')
        current_time = datetime.datetime.now(ist)
        users_exist = list(self.users_collection.find({"$or": [{"email_id": from_user}, {"email_id": to_user}]}))
        if len(users_exist) != 2:
            return Response({"detail": "One or both users do not exist."}, status=status.HTTP_400_BAD_REQUEST)
        if len(self.request_count[from_user]) >= 3 and \
                current_time - self.request_count[from_user][0] < datetime.timedelta(seconds=60):
            return Response({"detail": "Rate limit exceeded"}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        self.request_count[from_user] = [timestamp for timestamp in self.request_count[from_user] if
                                         current_time - timestamp < datetime.timedelta(seconds=60)]
        self.request_count[from_user].append(current_time)

        friend_request = {
            "from_user": from_user,
            "to_user": to_user,
            "status": "pending",
            "timestamp": current_time
        }
        self.friend_requests_collection.insert_one(friend_request)
        return Response({"detail": "Friend request sent"}, status=status.HTTP_201_CREATED)

    def accept_reject_friend_request(self, from_user, to_user, action):
        if not from_user or not to_user or action not in ['accept', 'reject']:
            return Response({"detail": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)

        new_status = 'accepted' if action == 'accept' else 'rejected'
        result = self.friend_requests_collection.update_one(
            {"from_user": from_user, "to_user": to_user, "status": "pending"},
            {"$set": {"status": new_status}}
        )

        if result.matched_count == 0:
            return Response({"detail": "Friend request not found"}, status=status.HTTP_404_NOT_FOUND)

        if new_status == 'accepted':
            self.users_collection.update_one({"email_id": from_user}, {"$addToSet": {"friends": to_user}})
            self.users_collection.update_one({"email_id": to_user}, {"$addToSet": {"friends": from_user}})

        return Response({"detail": f"Friend request {new_status}"}, status=status.HTTP_200_OK)


class FriendsListService:
    """
    RETURNS LIST OF FRIENDS USER HAVE
    """
    def __init__(self):
        self.users_collection = user_collection

    def list_friends(self, user_email):
        user = self.users_collection.find_one({"email_id": user_email})
        if not user:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        friends = user.get("friends", [])
        return Response({"friends": friends}, status=status.HTTP_200_OK)


class PendingFriendRequestsService:
    """
    RETURNS LIST OF PENDING FRIEND REQUEST
    """
    def __init__(self):
        self.friend_requests_collection = connect_collection

    def list_pending_requests(self, user_email):
        requests = self.friend_requests_collection.find({"to_user": user_email, "status": "pending"})
        serializer = FriendRequestSerializer(requests, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
