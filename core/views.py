import requests
from django.shortcuts import render
from django.views import View
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

response = requests.get(url='https://v6.exchangerate-api.com/v6/57103832bca2b0605120abcf/latest/USD').json()
# currencies = response.get('conversion_rates')
CURRENCIES = response.get('conversion_rates')


class HomeView(View):

    def get(self, request):
        context = {
            'currencies': CURRENCIES
        }
        return render(request, 'core/home.html', context)

    def post(self, request):
        from_amount = float(request.POST.get('amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((CURRENCIES[to_curr] / CURRENCIES[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': CURRENCIES,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='core/home.html', context=context)


###########################  API  #####################################################

class RatesAPIView(APIView):
    def get(self, requset):
        fr = requset.GET.get('from', '')
        to = requset.GET.get('to', '')
        value = requset.GET.get('value', '')
        print(fr, to, value)
        try:
            value = float(value)
        except:
            return Response({"error": "Incorrect value"})

        if fr not in CURRENCIES or to not in CURRENCIES:  # or not isinstance(value, (int, float))
            return Response({"error": "Incorrect Currency"})

        converted_amount = round((CURRENCIES[to] / CURRENCIES[fr]) * float(value), 2)
        return Response({'result': converted_amount})
