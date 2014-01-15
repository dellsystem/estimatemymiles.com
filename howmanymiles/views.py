import json
import string

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from howmanymiles.models import Airline, Alliance, MileageInfoSource, \
                                AccrualRule


def home(request):
    context = {
        'alliances': Alliance.objects.all(),
        'airlines': Airline.objects.all(),
        'fare_classes': string.uppercase,
    }

    return render(request, 'home.html', context)


def database(request):
    context = {
        'alliances': Alliance.objects.all(),
        'non_allied_airlines': Airline.objects.filter(alliance__isnull=True),
    }

    return render(request, 'database.html', context)


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


def operating_rules(request, earning_pk, operating_pk):
    earning_airline = get_object_or_404(Airline, pk=earning_pk)
    operating_airline = get_object_or_404(Airline, pk=operating_pk)

    fare_classes = []
    for letter in string.uppercase:
        rules = earning_airline.earning_rules.filter(
            fare_classes__contains=letter,
            operating_airline=operating_airline)
        fare_classes.append((letter, rules))

    try:
        rules_source = MileageInfoSource.objects.get(
            operating_airline=operating_airline,
            earning_airline=earning_airline)
    except MileageInfoSource.DoesNotExist:
        rules_source = None

    context = {
        'earning': earning_airline,
        'operating': operating_airline,
        'fare_classes': fare_classes,
        'rules_source': rules_source,
    }

    return render(request, 'airline/rules.html', context)


def rules_api(request, earning_pk, operating_pk, fare_class):
    accrual_rules = AccrualRule.objects.filter(earning_airline=earning_pk,
        operating_airline=operating_pk, fare_classes__contains=fare_class)
    data = []

    # This should be templated
    for rule in accrual_rules:
        data.append({
            'fare_name': rule.fare_name,
            'origin': rule.origin.name if rule.origin else 'Any',
            'destination': rule.destination.name if rule.origin else 'Any',
            'start_date': str(rule.start_date or '--'),
            'end_date': str(rule.end_date or '--'),
            'award_miles_percentage': rule.award_miles_percentage,
            'tier_miles_percentage': rule.award_miles_percentage,
            'num_segments': str(rule.num_segments),
            'standard_minimum': rule.standard_minimum,
            'elite_minimum': rule.elite_minimum,
        })

    return HttpResponse(json.dumps(data), content_type="application/json")
