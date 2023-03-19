from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.shortcuts import render
from analysis.models import Order
from django.core import serializers
from django.contrib.auth.decorators import login_required

@login_required(login_url = '/admin_login')
def dashboard_with_pivot(request):
    current = request.user
    if current.is_staff:
        return render(request, '', {})  #staff_dashboard.html



def pivot_data(request):
    dataset = Order.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)


   

