from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from howmanymiles.models import Alliance, Airline, FareClass, MileageMultiplier


DATE_FORMAT = '%Y-%m-%d'


class Command(BaseCommand):
    help = "Add mileage multiplier info for one fare bucket."

    def handle(self, *args, **options):
        write = self.stdout.write
        operating_airline = Airline.objects.get(pk=raw_input("Operating: "))
        earning_airline = Airline.objects.get(pk=raw_input("Earning: "))
        write("Using %s as the operating, %s as the earning." % (
            operating_airline, earning_airline))

        # Add multipliers in a loop
        while True:
            # Collect the info from the user.
            fare_name = raw_input("Fare name: ")
            booking_classes = raw_input("Booking classes, comma-separated: ")
            base_multiplier = raw_input("Base multiplier percentage: ")
            minimum_miles = raw_input("Minimum miles: ")

            if earning_airline.qualifying_miles_name:
                qualifying_multiplier = raw_input("Qualifying multiplier "
                    "percentage: ")
                qualifying_segments = raw_input("Qualifying segments: ")

            start_date = raw_input("Start date: ")
            end_date = raw_input("End date: ")
            other_restrictions = raw_input("Other restrictions: ")
            only_elites = raw_input("Only elites? y for yes: ")

            # Convert things to the right type, if necessary
            base_multiplier = int(base_multiplier)
            minimum_miles = int(minimum_miles) if minimum_miles else 0

            if start_date:
                start_date = datetime.strptime(start_date, DATE_FORMAT)
            else:
                start_date = None

            if end_date:
                end_date = datetime.strptime(end_date, DATE_FORMAT)
            else:
                end_date = None

            only_elites = 'y' in only_elites

            # Now process the information and add it to the database.
            multipliers = []
            class_codes = [c.strip() for c in booking_classes.split(',')]
            for class_code in class_codes:
                write("Class code: %c" % class_code)
                fare_class = FareClass.objects.get_or_create(
                    operating_airline=operating_airline,
                    earning_airline=earning_airline,
                    class_code=class_code)[0]

                multiplier = MileageMultiplier.objects.create(
                    fare_name=fare_name.strip(),
                    fare_class=fare_class,
                    base_multiplier=base_multiplier,
                    minimum_miles=minimum_miles,
                    start_date=start_date,
                    end_date=end_date,
                    only_elites=only_elites,
                    other_restrictions=other_restrictions)

                # Only save qualifying info if the airline has such a thing
                if earning_airline.qualifying_miles_name:
                    multiplier.qualifying_miles = int(qualifying_miles)
                    multiplier.qualifying_segments = float(qualifying_segments)
                    multiplier.save()

                multipliers.append(multiplier)

            write("Done! Created %d multipliers:" % len(multipliers))
            for multiplier in multipliers:
                write("- %s" % multiplier)

            quit = raw_input("Type q to quit, enter to continue: ")
            if quit.strip() == 'q':
                write("Quitting.")
                break
