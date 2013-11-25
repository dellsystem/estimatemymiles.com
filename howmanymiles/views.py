from django.shortcuts import render

from howmanymiles.models import Airline


def home(request):
    airlines = Airline.objects.get_traveling()
    context = {
        'airlines': airlines,
    }

    return render(request, 'home.html', context)
