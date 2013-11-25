from django.shortcuts import render

from howmanymiles.models import Airline


def home(request):
    context = {
        'traveling_airlines': Airline.objects.get_traveling(),
        'all_airlines': Airline.objects.all(),
    }

    return render(request, 'home.html', context)
