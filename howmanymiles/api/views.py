from django.shortcuts import get_object_or_404
from jsonview.decorators import json_view

from howmanymiles.models import Airline, FareClass


@json_view
def fareclasses(request, airline_pk):
    airline = get_object_or_404(Airline, pk=airline_pk)
    fare_classes = []
    for fare_class in airline.fareclass_set.all():
        fare_classes.append({
            'pk': fare_class.pk,
            'class_code': fare_class.class_code,
        })
    return fare_classes


@json_view
def mileages(request, fareclass_pk):
    fareclass = get_object_or_404(FareClass, pk=fareclass_pk)

    airlines = {}
    for mileage in fareclass.mileagemultiplier_set.order_by('-accrual_factor'):
        airline = mileage.earning_airline

        if airline.pk not in airlines:
            airlines[airline.pk] = {
                'name': str(airline),
                'ff_program': airline.ff_program,
                'mileages': []
            }

        airlines[airline.pk]['mileages'].append({
            'restrictions': mileage.restrictions,
            'fare_name': mileage.fare_name,
            'qualifying_miles': mileage.get_qualifying_miles(),
            'qualifying_segments': mileage.get_qualifying_segments(),
            'accrual_factor': mileage.get_accrual_factor(),
            'minimum_miles': mileage.minimum_miles or 'N/A',
        })

    return airlines
