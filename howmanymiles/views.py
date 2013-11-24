from django.shortcuts import render

from howmanymiles.models import Alliance


def home(request):
    alliances = Alliance.objects.all()
    context = {
        'alliances': alliances,
    }

    return render(request, 'home.html', context)
