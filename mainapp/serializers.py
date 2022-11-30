from .models import User
from rest_framework import serializers
from .models import Profile, Transaction
from rest_framework.reverse import reverse

from django.contrib.sites.shortcuts import get_current_site

class BrokerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username','password')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        user.profile.profile_type = 3
        user.profile.createdBy = self.context['request'].user
        user.save()
        # setting this to none so it doesn't get returned with the user instance
        user.password = None
        return user

class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username','password')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        user.profile.profile_type = 4
        user.profile.createdBy = self.context['request'].user
        user.save()
        # setting this to none so it doesn't get returned with the user instance
        user.password = None
        return user

class ManagerCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'username','password')
        read_only_fields = ('pk',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()
        user.profile.profile_type = 2
        user.profile.createdBy = self.context['request'].user
        user.save()
        # setting this to none so it doesn't get returned with the user instance
        user.password = None
        return user

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserProfileListSerializer(serializers.ModelSerializer):
    user = UserListSerializer()
    profile_type = serializers.SerializerMethodField()
    class Meta:
        model = Profile
        fields = ['pk', 'user', 'points', 'profile_type']
    
    def get_profile_type(self, obj):
        if obj.profile_type == 1:
            return "admin"
        if obj.profile_type == 2:
            return "manager"
        if obj.profile_type == 3:
            return "broker"
        if obj.profile_type == 4:
            return "user"

class AddPointsSerializer(serializers.Serializer):
        recevier = serializers.IntegerField()
        amount = serializers.IntegerField()
    
class TransactionSerializer(serializers.ModelSerializer):
    sender = UserProfileListSerializer()
    receiver = UserProfileListSerializer()
    transaction_type = serializers.SerializerMethodField()
    amount = serializers.SerializerMethodField()
    date = serializers.DateTimeField()
    class Meta:
        model = Transaction
        fields = ['pk', 'sender', 'receiver', 'amount', 'transaction_type', 'date']
    
    def get_transaction_type(self, obj):
        if obj.transaction_type == 1:
            return "points top up"
        if obj.transaction_type == 2:
            return "bet on number " + str(obj.selected_number)
        if obj.transaction_type == 3:
            return "won prize"
        if obj.transaction_type == 4:
            return "Withdraw"
        if obj.transaction_type == 5:
            return "commision"
    def get_amount(self, obj):
        if obj.transaction_type == 1:
            return "+" + str(obj.amount)
        if obj.transaction_type == 2:
            return "-" + str(obj.amount)
        if obj.transaction_type == 3:
            return "+" + str(obj.amount)
        if obj.transaction_type == 4:
            return "-" + str(obj.amount)
        if obj.transaction_type == 5:
            return "+" + str(obj.amount)

class BetSerializer(serializers.Serializer):
    selected_number = serializers.IntegerField(required=True)
    amount = serializers.IntegerField(required=True)
    gameID = serializers.IntegerField(required=True)


