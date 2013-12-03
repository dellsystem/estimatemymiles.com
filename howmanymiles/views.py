from django.shortcuts import render, get_object_or_404

from howmanymiles.models import Airline, Alliance


def home(request):
    context = {
        'traveling_airlines': Airline.objects.get_traveling(),
        'all_airlines': Airline.objects.all(),
    }

    return render(request, 'home.html', context)


def progress(request):
    context = {
        'alliances': Alliance.objects.all(),
    }

    return render(request, 'progress.html', context)


def progress_detail(request, operating, earning):
    operating = get_object_or_404(Airline, pk=operating)
    earning = get_object_or_404(Airline, pk=earning)
    fare_classes = operating.fare_classes.filter(earning_airline=earning)

    context = {
        'operating': operating,
        'earning': earning,
        'fare_classes': fare_classes,
    }
    return render(request, 'progress_detail.html', context)
