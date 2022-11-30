from django.shortcuts import render
from .serializers import BetSerializer, TransactionSerializer, ManagerCreateSerializer, BrokerCreateSerializer, UserCreateSerializer, UserProfileListSerializer, AddPointsSerializer
from .permissions import IsAdminOrReadOnly, IsBrokerOrReadOnly, IsAuthenticatedOrReadOnly, IsManagerOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from rest_framework.views import APIView
from .models import Profile, Transaction, BetEntry
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import ResultSettings
import json
# Create your views here.

# view for creating broker accounts
class CreateBrokerView(generics.CreateAPIView):
    # only admins and brokers can create broker accounts
    permission_classes = [IsAuthenticatedOrReadOnly & (IsAdminOrReadOnly | IsBrokerOrReadOnly)]
    serializer_class = BrokerCreateSerializer

class CreateUserView(generics.CreateAPIView):
    # only brokers can create user accounts
    permission_classes = [IsAuthenticatedOrReadOnly, IsBrokerOrReadOnly]
    
    serializer_class = UserCreateSerializer

class CreateManagerView(generics.CreateAPIView):
    # only brokers can create user accounts
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrReadOnly]
    serializer_class = ManagerCreateSerializer

class UserViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        queryset = Profile.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserProfileListSerializer(user)
        return Response(serializer.data)

class CurrentUserDetails(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        serializer = UserProfileListSerializer(request.user.profile)
        return Response(serializer.data)

class ListCreatedUsers(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        user = request.user
        createdUsers = Profile.objects.filter(createdBy=user)

        user_serializer = UserProfileListSerializer(createdUsers, many=True)

        return Response({
        'created_users': user_serializer.data,
    })

class ListAllUsers(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly & (IsAdminOrReadOnly | IsManagerOrReadOnly)]
    def get(self, request, **kwargs):
        user = request.user
        createdUsers = Profile.objects.filter(profile_type=4)

        user_serializer = UserProfileListSerializer(createdUsers, many=True)

        return Response({
        'created_users': user_serializer.data,
    })


class ListBrokers(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        user = request.user
        createdUsers = Profile.objects.filter(profile_type=3)

        user_serializer = UserProfileListSerializer(createdUsers, many=True)

        return Response({
        'broker_list': user_serializer.data,
    })

class GetIncomingTransactions(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        user = request.user
        incoming_transactions = Transaction.objects.filter(receiver=user.profile)

        transaction_serializer = TransactionSerializer(incoming_transactions, many=True)

        return Response({
        'incoming_transactions': transaction_serializer.data,
        })

class GetOutgoingTransactions(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        user = request.user
        outgoing_transactions = Transaction.objects.filter(sender=user.profile)

        transaction_serializer = TransactionSerializer(outgoing_transactions, many=True)

        return Response({
        'outgoing_transactions': transaction_serializer.data,
        })

class GetAllTransactions(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def get(self, request, **kwargs):
        user = request.user.profile
        transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user))
        transaction_serializer = TransactionSerializer(transactions, many=True)

        return Response({
        'transactions': transaction_serializer.data,
        })

class GetUserTransactions(APIView):
    permission_classes = [AllowAny]
    def get(self, request, **kwargs):
        pk = self.kwargs['pk']
        user = Profile.objects.get(pk=pk)
        transactions = Transaction.objects.filter(Q(sender=user) | Q(receiver=user))
        transaction_serializer = TransactionSerializer(transactions, many=True)

        return Response({
        'transactions': transaction_serializer.data,
        })

def percentage(percent, whole):
  return (percent * whole) / 100.0

class BetView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, format=None):
        serializer = BetSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.data["gameID"] == 1 or serializer.data["gameID"] == 2:
                voter_user = request.user.profile
                if voter_user.points >= serializer.data['amount']:
                    voter_user.points -= serializer.data['amount']
                    entry = BetEntry(voter=voter_user, selected_number=serializer.data['selected_number'], bet_amount=serializer.data['amount'], game_id=serializer.data['gameID'])
                    transaction = Transaction(sender=request.user.profile, receiver=request.user.profile, amount=serializer.data['amount'], transaction_type=2, selected_number=serializer.data['selected_number'])
                    voter_user.save()
                    entry.save()
                    transaction.save()

                    broker_percentage = percentage(ResultSettings.load().UserPercent, serializer.data['amount'])
                    voter_user.createdBy.profile.points += broker_percentage
                    voter_user.createdBy.profile.save()
                    transaction = Transaction(sender=voter_user.createdBy.profile, receiver=voter_user.createdBy.profile, amount=broker_percentage, transaction_type=5, selected_number=serializer.data['selected_number'])
                    transaction.save()

                    broker_percentage2 = percentage(ResultSettings.load().BrokerPercent, serializer.data['amount'])
                    voter_user.createdBy.profile.createdBy.profile.points += broker_percentage2
                    voter_user.createdBy.profile.createdBy.profile.save()
                    transaction2 = Transaction(sender=voter_user.createdBy.profile.createdBy.profile, receiver=voter_user.createdBy.profile.createdBy.profile, amount=broker_percentage2, transaction_type=5, selected_number=serializer.data['selected_number'])
                    transaction2.save()


                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "you don't have enough points to bet !"}, status=status.HTTP_403_FORBIDDEN)
            return Response({"error": "invalid game id !"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class BetStatusGame1(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        bet_numbers = [] # maps numbers to their total result, 0 is not used.
        # init the array with zeros...
        for i in range(0,10):
            bet_numbers.append(0)
        bets = BetEntry.objects.filter(game_id=1, isArchive=False)

        for bet in bets:
            bet_numbers[bet.selected_number] = bet_numbers[bet.selected_number] + bet.bet_amount
        
        return Response({"status":json.dumps(bet_numbers)}, status=status.HTTP_200_OK)

class NextResultTime(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        bet_settings = ResultSettings.load()
        return Response({"time":bet_settings.NextResult}, status=status.HTTP_200_OK)
class BetStatusGame2(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, **kwargs):
        bet_numbers = [] # maps numbers to their total result, 0 is not used.
        # init the array with zeros...
        for i in range(0,100):
            bet_numbers.append(0)
        bets = BetEntry.objects.filter(game_id=2, isArchive=False)

        for bet in bets:
            bet_numbers[bet.selected_number] = bet_numbers[bet.selected_number] + bet.bet_amount
        
        return Response({"status":json.dumps(bet_numbers)}, status=status.HTTP_200_OK)

class WithdrawPoints(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, format=None):
        serializer = AddPointsSerializer(data=request.data)
        if serializer.is_valid():
            receiver_user = get_object_or_404(Profile, pk=serializer.data['recevier'])

            if(request.user.profile.profile_type == 1):
                transaction = Transaction(sender=request.user.profile, receiver=receiver_user, amount=serializer.data['amount'], transaction_type=4)
                receiver_user.points = receiver_user.points - serializer.data['amount']
                transaction.save()
                receiver_user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif(request.user.profile.profile_type == 3):
                if(receiver_user.points >= serializer.data['amount']):
                    request.user.profile.points = request.user.profile.points + serializer.data['amount']
                    receiver_user.points = receiver_user.points - serializer.data['amount']
                    transaction = Transaction(sender=request.user.profile, receiver=receiver_user, amount=serializer.data['amount'], transaction_type=4)
                    transaction.save()
                    receiver_user.save()
                    request.user.profile.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "user don't have that much points !"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendPoints(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, request, format=None):
        serializer = AddPointsSerializer(data=request.data)
        if serializer.is_valid():
            receiver_user = get_object_or_404(Profile, pk=serializer.data['recevier'])

            #if the sender is an admin, add points (generate) directly....
            if(request.user.profile.profile_type == 1):
                transaction = Transaction(sender=request.user.profile, receiver=receiver_user, amount=serializer.data['amount'], transaction_type=1)
                receiver_user.points = receiver_user.points + serializer.data['amount']
                transaction.save()
                receiver_user.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            # if the sender is a broker, check if they have enough points then deduct from their amount
            # and send it to the receiver
            elif(request.user.profile.profile_type == 3):
                if(request.user.profile.points >= serializer.data['amount']):
                    request.user.profile.points = request.user.profile.points - serializer.data['amount']
                    receiver_user.points = receiver_user.points + serializer.data['amount']
                    transaction = Transaction(sender=request.user.profile, receiver=receiver_user, amount=serializer.data['amount'], transaction_type=1)
                    transaction.save()
                    receiver_user.save()
                    request.user.profile.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response({"error": "you don't have enough points to give !"}, status=status.HTTP_403_FORBIDDEN)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)