
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
    allied_earning_partners = set()
    other_earning_partners = set()

    context = {
        'airline': airline,
        'allied_earning_partners': allied_earning_partners,
        'other_earning_partners': other_earning_partners,
    }

    return render(request, 'airline/detail.html', context)
