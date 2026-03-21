from django.shortcuts import render, redirect
from .models import Fund, PaymentHistory
from django.contrib import messages
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def fund(request):
    funds = Fund.objects.all()
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address = request.POST.get('address')
        city = request.POST.get('city')
        pin = request.POST.get('pin')
        amount = request.POST.get('amount')
        
        fund_obj = Fund.objects.create(
            user = request.user,
            first_name = first_name,
            last_name = last_name,
            address = address,
            city = city,
            pin = pin,
            amount = amount
        )
        fund_obj.save()
        messages.success(request, 'Your Fund has been given successfully.')
        return redirect('checkout', fund_obj.id)
    return render(request, 'fund/fund.html', {'funds': funds})


def CheckoutViewSession( request, pk ):
    fund = Fund.objects.get( id = pk )
    YOUR_WEBSITE_URL = settings.YOUR_WEBSITE_URL
    
    checkout_session = stripe.checkout.Session.create(
        payment_method_types = ['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'unit_amount': int(fund.amount)*100,
                    'product_data': {
                        'name': 'Fund',
                        'description': 'This is fund for nobel cause',
                    },
                },
                'quantity': 1, 
            }
        ],
        metadata = {
            'fund_id': pk,
            'user_username': request.user.username,
            'user_email': request.user.email, 
        },
        mode = 'payment',
        success_url = YOUR_WEBSITE_URL + f"/success-page/{pk}",
        cancel_url = YOUR_WEBSITE_URL + f"/fund",          
    )
    return redirect(checkout_session.url)

def success_page( request, pk ):
    return render(request, 'fund/success_page.html')

def fail_page( request ):
    return render(request, 'fund/fail_page.html')

@csrf_exempt
def stripe_webhook(request):
    event = None
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    
    print('Signature Header is received:' ,sig_header)
    print('Payload is received:', payload)
    print('Webhook Secret:', settings.STRIPE_WEBHOOK_SECRET)
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError as e:
        print("Stripe webhook payload error:", e)
        return HttpResponse( status = 400 )
    except stripe.error.SignatureVerificationError as e:
        print("Stripe webhook signature error:", e)
        return HttpResponse( status = 400 )
    
    if event['type'] == 'checkout.session_async_payment_failed':
        
        session = event['data']['object']
        
        fund_id = session['metadata']['fund_id']
        get_fund_id = Fund.objects.get( id = fund_id )
        
        user_username = session['metadata']['user_username']
        get_user_username = User.objects.get( username = user_username )
        
        user_email = session['metadata']['user_email']
        get_user_email = User.objects.get( email = user_email )
        
        PaymentHistory.objects.create(
            user = get_user_username,
            fund_amount = get_fund_id.amount,
        )
        
    elif event['type'] == 'checkout.session.completed':
        
        session = event['data']['object']
        
        fund_id = session['metadata']['fund_id']
        get_fund_id = Fund.objects.get( pk = fund_id )
        
        user_username = session['metadata']['user_username']
        get_user_username = User.objects.get( username = user_username )
        
        user_email = session['metadata']['user_email']
        get_user_email = User.objects.get( email = user_email )
        
        PaymentHistory.objects.create(
            user = get_user_username,
            fund_amount = get_fund_id.amount,
            status = True,
        )
        
    else:
        print('Unhandled event type{}'.format( event['type'] ) )
    return HttpResponse( status = 200 )