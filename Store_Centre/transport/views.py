
from django.conf import settings
from django.shortcuts import redirect, render
from transport.models import *
from transport.forms import *
from django.contrib.auth.decorators import login_required
import requests,json
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from decimal import Decimal
from paypal.standard.forms import PayPalPaymentsForm

from django_daraja.mpesa.core import MpesaClient
from django.http import HttpResponse, HttpResponseRedirect
from django.http.response import JsonResponse
from django.urls import reverse
from requests.api import get
from requests.auth import HTTPBasicAuth
from django.shortcuts import render
from django.http import HttpResponse




# @login_required(login_url='client_login')
def request_transport(request):
    #api_key = 'AIzaSyBGxCnx-pYsfygMM9mDP6EjtJuoBJ3zoo'
    api_key = 'AIzaSyDsBaerWzN5SHic00SOOpMpiREUYuyiii'
    initial_units=request.session.get('initial_units')
    final_units = request.session.get('final_units')
    if request.method == 'POST':
        form = TransportForm(request.POST)
        if form.is_valid():
            transport_request = form.save(commit=False)
            transport_request.user = request.user
            #client goods logic
            goods = Goods.objects.filter(owner=request.user).last()
            transport_request.goods= goods
            #distance matrix logic
            source = 'Nairobi'
            destination = transport_request.address
            destination1='Embu'
            url = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
            
            r = requests.get(url + 'origins=' + source +
                '&destinations=' + destination1 +
                '&key=' + api_key)
            
            # r =requests.get(url)            
            # data = r.read()
            # name=data.decode("utf-8")
            # conv = json.loads(name)
            # print(conv)
            
            x=r.json()
            print(x)
            
            distance = x['rows'][0]["elements"][0]["distance"]["value"]
            print(distance)
            transport_request.distance = (distance)/1000
            #calculate price
            price = (transport_request.distance)*200
            transport_request.price = price
            #transport_type logic
            if initial_units > final_units:
                transport_request.transport_type = Transport.PICKUP
            elif final_units > initial_units:
                transport_request.transport_type= Transport.DELIVERY
            transport_request.save()
            return redirect('request_summary')
        else:
            print(form.errors)
    else:
        form =TransportForm()
    context = {
        'form':form,
        'api_key': api_key,
        'initial_units':initial_units,
        'final_units': final_units,
    }
    return render(request,'request_transport.html',context) #, context

# @login_required(login_url='client_login')
def request_summary(request):
    request_transport = Transport.objects.filter(user=request.user).last()
    
    print(request_transport.user.first_name)
    context = {
        'request_transport': request_transport,
    }
    
    #email logic
    subject = 'TRANSPORT REQUEST SUMMARY'
    message = get_template('transport_summary_email.html').render(context)
    msg = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [request_transport.email],
    )
    msg.content_subtype = 'html'
    msg.send()
    
    return render(request,'request_summary.html',context)  #, context


# @login_required(login_url='client_login')
def summaries(request):
    # all_summaries = Transport.objects.all().order_by('-created')
    # summaries = Transport.objects.filter(user=request.user).all().order_by('-created')
    # context = {
    #     'summaries': summaries,
    #     'all_summaries': all_summaries,
    # }
    
    
    return render(request,'summaries.html') #, context



cl = MpesaClient()
stk_push_callback_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
b2c_callback_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v1/paymentrequest'
c2b_callback_url = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl'



#newapi configuration
# def initiate_payment(request):
#     access_token = "your_access_token_here" # replace with your actual access token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    
#     headers = { "Authorization": "Bearer %s" % access_token }
    
#     # replace with your actual data
#     payload = {
#         "BusinessShortCode": "your_business_short_code_here",
#         "Password": "your_encoded_password_here",
#         "Timestamp": "your_timestamp_here",
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": "10",
#         "PartyA": "your_phone_number_here",
#         "PartyB": "your_business_short_code_here",
#         "PhoneNumber": "your_phone_number_here",
#         "CallBackURL": "your_callback_url_here",
#         "AccountReference": "your_account_reference_here",
#         "TransactionDesc": "your_transaction_description_here"
#     }
    
#     response = requests.post(api_url, json=payload, headers=headers)
    
#     return HttpResponse(response.text)

def getAccessToken(request):
    consumer_key = 'A3G5KRHlUd0vk4xrXwoDDchCIDq4vAoT'
    consumer_secret = 'J7wEjNfxbSzPogLm'
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)
    

def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)
    

def stk_push_success(request, ph_number, totalAmount):
    phone_number = ph_number
    amount = totalAmount
    account_reference = 'modern warehouse'
    transaction_desc = 'STK Push Description'
    callback_url = stk_push_callback_url
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)



# @login_required(login_url='client_login')
def payment(request):
    request_transport = Transport.objects.filter(user=request.user).last()
    request_goods = Goods.objects.filter(owner=request.user).last()  
    paypal_client_id = settings.PAYPAL_CLIENT_ID
    context = {
        'request_transport': request_transport,
        'request_goods': request_goods,
        'paypal_client_id': paypal_client_id
        
    }
    if request.method == 'POST':
        name=request.POST.get('fname')
        phone_number=request.POST.get('phone_number')
        amount=request.POST.get('amount')

        ph_number = None
        totalAmount = int(float(amount))

        if phone_number[0] == '0':
            ph_number = '254'+ phone_number[1:]
        elif phone_number[0:2] == '254':
            ph_number = phone_number
        else:
            # messages.error(request, 'Check you Phone Number format 2547xxxxxxxx')
            return redirect(request.get_full_path())


        stk_push_success(request, ph_number, totalAmount)
        request_transport.is_paid = True
        request_transport.save()
        return render (request,'success.html')

    if request.GET:
        input_value = request.GET['paypal_transaction']
        if input_value:
            request_transport.is_paid = True
            request_transport.save()
            return render (request,'success.html')


    return render(request,'payment.html', context)

def approval(request, request_summary_id):
    request_summary = Transport.objects.filter(id=request_summary_id).first()
    request_summary.is_approved = True
    request_summary.save()
    context ={
        'request_summary':request_summary
    }
    #email logic
    subject = 'TRANSPORT REQUEST APPROVAL'
    message = get_template('transport_approval_email.html').render(context)
    msg = EmailMessage(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [request_summary.email],
    )
    msg.content_subtype = 'html'
    msg.send()

    return redirect('transport_summaries')
    
