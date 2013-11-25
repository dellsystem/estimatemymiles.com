from django.core.management.base import BaseCommand, CommandError

from howmanymiles.models import Alliance, Airline, FareClass, MileageMultiplier


class Command(BaseCommand):
    help = "Add mileage multiplier info for one fare bucket."

    def handle(self, *args, **options):
        write = self.stdout.write
        earning_airline = Airline.objects.get(pk=raw_input("Enter the code of "
            "the airline/FF program you wish to accrue miles on: "))

        # Add multipliers in a loop
        while True:
            write("Using %s as the accruing airline." % earning_airline)
            # Collect the info from the user.
            operating_airline = Airline.objects.get(pk=raw_input("Enter the "
                "code of the operating airline: "))
            fare_name = raw_input("Enter the human-readable fare class name: ")
            booking_classes = raw_input("Enter the booking classes, separated "
                                        "with commas: ")
            accrual_factor = raw_input("Enter the accrual factor, as a "
                                        "percentage but without the % sign "
                                        "(e.g., 100): ")
            minimum_miles = raw_input("Enter the minimum number of miles "
                                      "earned for this fare class: ")
            if earning_airline.qualifying_miles_name is not None:
                qualifying_miles = raw_input("Enter the qualifying miles, as "
                                             "a percentage but without the % "
                                             "sign: ")
                qualifying_segments = raw_input("Enter the number of "
                                                "qualifying segments: ")

            restrictions = raw_input("Enter restrictions for this fare class, "
                                     "if any: ").strip()

            # Now process the information and add it to the database.
            multipliers = []
            class_codes = [c.strip() for c in booking_classes.split(',')]
            for class_code in class_codes:
                fare_class = FareClass.objects.get_or_create(
                    airline=operating_airline,
                    class_code=class_code)[0]

                multiplier = MileageMultiplier.objects.create(
                    earning_airline=earning_airline,
                    fare_class=fare_class,
                    restrictions=restrictions,
                    accrual_factor=int(accrual_factor),
                    minimum_miles=int(minimum_miles) if minimum_miles else 0,
                    fare_name=fare_name.strip())

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
