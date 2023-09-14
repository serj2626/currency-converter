import requests
from django.shortcuts import render
from django.views import View


class HomeView(View):
    response = requests.get(url='https://v6.exchangerate-api.com/v6/57103832bca2b0605120abcf/latest/USD').json()
    currencies = response.get('conversion_rates')

    def get(self, request):
        context = {
            'currencies': self.currencies
        }
        return render(request, 'core/home.html', context)

    def post(self, request):
        from_amount = float(request.POST.get('amount'))
        from_curr = request.POST.get('from-curr')
        to_curr = request.POST.get('to-curr')

        converted_amount = round((self.currencies[to_curr] / self.currencies[from_curr]) * float(from_amount), 2)

        context = {
            'from_curr': from_curr,
            'to_curr': to_curr,
            'from_amount': from_amount,
            'currencies': self.currencies,
            'converted_amount': converted_amount
        }

        return render(request=request, template_name='core/home.html', context=context)
