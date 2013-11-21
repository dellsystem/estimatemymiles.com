from django.db import models


class Alliance(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Airline(models.Model):
    name = models.CharField(max_length=100)
    short_code = models.CharField(max_length=2, primary_key=True)
    alliance = models.ForeignKey(Alliance)
    ff_program = models.CharField(max_length=100, help_text="The name of the "
        "frequent flyer program associated with this airline.")
    qualifying_miles_name = models.CharField(max_length=100, help_text="e.g., "
        "'Altitude' for Air Canada. Leave empty if none.", null=True,
        blank=True)

    def __unicode__(self):
        return self.name


class FareClass(models.Model):
    airline = models.ForeignKey(Airline)
    class_code = models.CharField(max_length=1)

    class Meta:
        verbose_name_plural = 'Fare classes'
        unique_together = ('airline', 'class_code')

    def __unicode__(self):
        return "%s - %s" % (self.airline, self.class_code)


class MileageMultiplier(models.Model):
    earning_airline = models.ForeignKey(Airline)
    fare_class = models.ForeignKey(FareClass)
    restrictions = models.TextField(blank=True, null=True)
    accrual_factor = models.IntegerField(help_text="As a percentage.")
    minimum_miles = models.IntegerField(default=0)
    fare_name = models.CharField(max_length=100, help_text="The human-readable "
        "name for the fare class, according to the earning airline. E.g., "
        "'Economy class' or 'Business class'.", null=True, blank=True)
    qualifying_miles = models.IntegerField(help_text="As a percentage. Leave "
        "empty if the airline doesn't have a special elite program (e.g., "
        "Aegean).", blank=True, null=True)
    qualifying_segments = models.DecimalField(max_digits=2, decimal_places=1,
        help_text="Usually 1. Leave empty if the airline doesn't have a "
        "special elite program (e.g., Aegean).", blank=True, null=True)

    def __unicode__(self):
        return "%s, earning with %s (%d%%)" % (self.fare_class,
                                               self.earning_airline,
                                               self.accrual_factor)
