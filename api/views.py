from random import random

from django.shortcuts import render, get_object_or_404

# Create your views here.
# api/views.py
from django.http import JsonResponse
import random
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from django.shortcuts import render
from api.models import Campaign
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Campaign, Donation
from .serializers import CampaignSerializer, DonationSerializer, UserSerializer
otp_storage = {}
verified_users = set()
users_db = {}

@api_view(['POST'])
def send_otp(request):
    email = request.GET.get('email')
    otp = str(random.randint(100000, 999999))

    send_mail(
        'Your OTP Code',
        f'Your OTP is {otp}',
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
    )

    return JsonResponse({'message': 'OTP sent to email'})
# VERIFY OTP
def verify_otp(request):
    email = request.GET.get('email')
    user_otp = request.GET.get('otp')

    if email in otp_storage and str(otp_storage[email]) == user_otp:
        verified_users.add(email)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'failed'})

# REGISTER
def register_user(request):
    return render(request, 'frontend/register.html')
    username = request.GET.get('username')
    email = request.GET.get('email')
    password = request.GET.get('password')

    if email not in verified_users:
        return JsonResponse({'status': 'verify_email_first'})

    if username in users_db:
        return JsonResponse({'status': 'user_exists'})

    users_db[username] = {
        'email': email,
        'password': make_password(password)
    }

    return JsonResponse({'status': 'registered'})
def verify_and_register(request):
    email = request.GET.get('email')
    otp = request.GET.get('otp')

    if otp_storage.get(email) != otp:
        return JsonResponse({'error': 'Invalid OTP'})

    # ✅ Create user if not exists
    user, created = User.objects.get_or_create(
        username=email,
        defaults={'email': email}
    )

    # Set unusable password (since OTP login)
    user.set_unusable_password()
    user.save()

    # ✅ Auto login
    login(request, user)

    return JsonResponse({'message': 'Registration successful'})
def home(request):
    return render(request, 'frontend/index.html')



class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all().order_by('-created_at')
    serializer_class = CampaignSerializer

    def get_permissions(self):
        if self.action in ['create','update','partial_update','destroy','donate']:
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=True, methods=['post'])
    def donate(self, request, pk=None):
        campaign = self.get_object()
        amount = request.data.get('amount')
        try:
            amount = int(amount)
        except:
            return Response({'error':'invalid amount'}, status=400)
        if amount <= 0:
            return Response({'error':'amount must be > 0'}, status=400)
        donation = Donation.objects.create(campaign=campaign, donor=request.user, amount=amount)
        return Response({
            'status':'donated',
            'donation': DonationSerializer(donation).data,
            'campaign': CampaignSerializer(campaign).data
        })

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all().order_by('-donated_at')
    serializer_class = DonationSerializer
    permission_classes = [IsAuthenticated]


# LOGIN
def login_user(request):
    username = request.GET.get('username')
    password = request.GET.get('password')

    if username not in users_db:
        return JsonResponse({'status': 'no_user'})

    stored_password = users_db[username]['password']

    if check_password(password, stored_password):
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'wrong_password'})
def donate(request):
    return render(request,'frontend/donate.html')
def campaign_details(request, id):
    campaign = get_object_or_404(Campaign, id=id)
    return render(request, 'frontend/campaign_details.html', {'campaign': campaign})

def home(request):
    return render(request,"frontend/index.html")

def donate(request):
    return render(request,'frontend/donate.html')

def campaigns(request):
    campaigns = Campaign.objects.all()
    return render(request,'frontend/campaigns.html',{'campaigns':campaigns})

def campaign_details(request,id):
    campaign = Campaign.objects.get(id=id)
    return render(request,'frontend/campaign_details.html',{'campaign':campaign})