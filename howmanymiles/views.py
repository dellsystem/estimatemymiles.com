
from django.shortcuts import render, get_object_or_404

from howmanymiles.models import Airline, Alliance


def home(request):
    context = {
        'alliances': Alliance.objects.all(),
        'non_allied_airlines': Airline.objects.filter(alliance__isnull=True),
    }

    return render(request, 'home.html', context)


def airline_detail(request, pk):
    airline = get_object_or_404(Airline, pk=pk)
    allied_earners, other_earners = airline.get_earning_partners()
    allied_operators, other_operators = airline.get_operating_partners()

    context = {
        'airline': airline,
        'allied_earners': allied_earners,
        'other_earners': other_earners,
        'allied_operators': allied_operators,
        'other_operators': other_operators,
    }

    return render(request, 'airline/detail.html', context)
