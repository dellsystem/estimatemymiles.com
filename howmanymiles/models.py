from django.conf import settings
from django.db import models


class Alliance(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_image_url(self):
        return settings.STATIC_URL + 'img/alliance/' + self.slug + '.png'


class AirlineManager(models.Manager):
    def get_traveling(self):
        """
        Returns all airlines with associated fare classes (which are associated
        with MileageMultiplier objects).
        """
        return self.annotate(num=models.Count('fareclass')) \
            .filter(num__gt=0)


class Airline(models.Model):
    objects = AirlineManager()
    name = models.CharField(max_length=100)
    short_code = models.CharField(max_length=2, primary_key=True)
    alliance = models.ForeignKey(Alliance, null=True, blank=True)
    ff_program = models.CharField(max_length=100, help_text="The name of the "
        "frequent flyer program associated with this airline.")
    qualifying_miles_name = models.CharField(max_length=100, help_text="e.g., "
        "'Altitude' for Air Canada. Leave empty if none.", null=True,
        blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.short_code)

    def get_qualifying_miles_name(self):
        if self.qualifying_miles_name:
            return "%s Qualifying Miles (%sQM)" % (self.qualifying_miles_name,
                self.qualifying_miles_name[0].upper())
        else:
            return "No qualifying miles"

    def get_qualifying_segments_name(self):
        if self.qualifying_miles_name:
            return "%s Qualifying Segments (%sQS)" % (
                self.qualifying_miles_name,
                self.qualifying_miles_name[0].upper())
        else:
            return "No qualifying segments"

    def get_image_url(self):
        return settings.STATIC_URL + 'img/airline/' + self.pk + '.png'


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

    def get_num_miles(self, base_miles, is_qualifying=False):
        factor = self.qualifying_miles if is_qualifying else self.accrual_factor
        return max(base_miles * factor / 100.0, self.minimum_miles)

    def get_qualifying_miles(self):
        if self.qualifying_miles is not None:
            return "%d%%" % self.qualifying_miles,
        else:
            return 'N/A'

    def get_qualifying_segments(self):
        if self.qualifying_segments is not None:
            return str(self.qualifying_segments)
        else:
            return 'N/A'

    def get_accrual_factor(self):
        return "%d%%" % self.accrual_factor
