from django.shortcuts import render

# Create your views here.
def order_list(request):
    return render(request, 'orders/list.html', {})
