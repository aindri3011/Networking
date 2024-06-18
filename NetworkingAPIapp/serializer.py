from rest_framework import serializers


# SERIALIZER TO CREATE USER SIGNUP
class CreateLoginSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=50, required=True)
    email_id = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)
    friends = serializers.ListField(child=serializers.EmailField(), required=False,
                                    default=list )


# SERIALIZER FOR LOGIN
class LoginSerializer(serializers.Serializer):

    email_id = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


# SERIALIZER FOR USER SEARCH INFORMATION
class UserSerializer(serializers.Serializer):

    email_id = serializers.EmailField()
    name = serializers.CharField(max_length=100)


# SERIALIZER FOR FRIEND REQUEST INFORMATION
class FriendRequestSerializer(serializers.Serializer):

    from_user = serializers.EmailField()
    to_user = serializers.EmailField()
    status = serializers.ChoiceField(choices=['pending', 'accepted', 'rejected'])
