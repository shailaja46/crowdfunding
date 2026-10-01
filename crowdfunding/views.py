import random
import json
from django.http import JsonResponse
from django.shortcuts import render
from api.models import Campaign 
from api.models import Donation
from django.contrib.auth.models import User
from django.contrib.auth import login

otp_storage = {}
verified_users = set()
users_db = {}


def register_page(request):
    return render(request,'register.html')
def login_page(request):
    return render(request, 'login.html')
def home(request):
    return render(request, 'frontend/index.html')
def send_otp(request):
    email = request.GET.get('email')

    if not email:
        return JsonResponse({'error': 'Email required'})

    otp = str(random.randint(100000, 999999))
    otp_storage[email] = otp
    print(f"OTP for {email}: {otp}")
    print(f"OTP for {email}: {otp}")  # For testing

    return JsonResponse({'message': 'OTP sent successfully'})


def verify_otp(request):
    email = request.GET.get('email')
    otp = request.GET.get('otp')

    if otp_storage.get(email) == otp:
        verified_users.add(email)
        return JsonResponse({'message': 'OTP verified'})
    else:
        return JsonResponse({'error': 'Invalid OTP'})

def register_user(request):

    if request.method == "POST":
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if email not in verified_users:
            return JsonResponse({'error': 'Verify OTP first'})
        return JsonResponse({'message': 'User registered successfully'})
    return render(request, "frontend/register.html")

    # ✅ ADD THIS PART (VERY IMPORTANT)
    return JsonResponse({'error': 'Invalid request method'})
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


    # ✅ Create user if not exists
    

def api_campaigns(request):
    campaigns = list(Campaign.objects.values())
    return JsonResponse(campaigns, safe=False)  
def api_donations(request):
    donations = list(Donation.objects.values())
    return JsonResponse(donations, safe=False)  
def home(request):
    return render(request,'frontend/index.html')

def donate(request):
    return render(request,'frontend/donate.html')

def campaigns(request):
    return render(request,'frontend/campaigns.html')

def campaign_details(request, id):
    campaign = Campaign.objects.get(id=id)
    return render(request,'frontend/campaign_details.html', {'campaign': campaign})
   