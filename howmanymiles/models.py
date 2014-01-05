from django.conf import settings
from django.db import models


class Alliance(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

    def get_image_url(self):
        return settings.STATIC_URL + 'img/alliance/' + self.slug + '.png'


class Airline(models.Model):
    name = models.CharField(max_length=100)
    short_code = models.CharField(max_length=2, primary_key=True)
    alliance = models.ForeignKey(Alliance, null=True, blank=True)
    ff_program = models.CharField(max_length=100, help_text="The name of the "
        "frequent flyer program associated with this airline.")
    qualifying_miles_name = models.CharField(max_length=100, help_text="e.g., "
        "'Altitude' for Air Canada. Leave empty if none.", null=True,
        blank=True)
    comments = models.TextField(blank=True, null=True, help_text="Any "
        "additional comments about mileage accumulation with this airline.")

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return "%s (%s)" % (self.name, self.short_code)

    def get_ff_program_name(self):
        return "%s %s" % (self.name, self.ff_program)

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

    def get_partner_statuses(self):
        statuses = []
        for airline in self.alliance.airline_set.all():
            count = self.fare_classes.filter(earning_airline=airline).count()

            if count == 26:
                status = 'done'
            elif count > 0:
                status = 'some'
            else:
                status = 'none'

            statuses.append((airline, status, count))

        return statuses


class MileageInfoSource(models.Model):
    operating_airline = models.ForeignKey(Airline,
        related_name='operating_sources')
    earning_airline = models.ForeignKey(Airline,
        related_name='earning_sources')
    link = models.URLField()

    class Meta:
        unique_together = ('operating_airline', 'earning_airline')

    def __unicode__(self):
        return "%s, earning with %s" % (self.operating_airline,
            self.earning_airline)


class FareClass(models.Model):
    operating_airline = models.ForeignKey(Airline, related_name='fare_classes')
    class_code = models.CharField(max_length=1)
    earning_airline = models.ForeignKey(Airline, related_name='+')

    class Meta:
        ordering = ['operating_airline', 'class_code']
        verbose_name_plural = 'Fare classes'
        unique_together = ('operating_airline', 'class_code',
            'earning_airline')

    def __unicode__(self):
        return "%s - %s, earning with %s" % (self.operating_airline,
            self.class_code, self.earning_airline)

    def covers_non_elites(self):
        return self.multipliers.filter(only_elites=False).exists()

    def covers_all_times(self):
        # If there's one that covers all times, great
        multipliers = self.multipliers
        if multipliers.filter(start_date__isnull=True, end_date__isnull=True):
            return True

        # Otherwise, make sure that there is one with a null start, and one with
        # a null end
        if not (multipliers.filter(start_date__isnull=True).exists() and
                multipliers.filter(end_date__isnull=True).exists()):
            return False
        else:
            # Good enough for now
            return True

    def covers_all_restrictions(self):
        multipliers_with_restrictions = self.multipliers.filter(
            models.Q(other_restrictions__isnull=False)).exclude(
            other_restrictions='')
        num = multipliers_with_restrictions.count()
        return num == 0 or num > 1


class MileageMultiplier(models.Model):
    fare_class = models.ForeignKey(FareClass, related_name='multipliers')
    base_multiplier = models.IntegerField(help_text="As a percentage.")
    minimum_miles = models.IntegerField(default=0)
    qualifying_multiplier = models.IntegerField(help_text="As a percentage. Leave "
        "empty if the airline doesn't have a special elite program (e.g., "
        "Aegean).", blank=True, null=True)
    qualifying_segments = models.DecimalField(max_digits=2, decimal_places=1,
        help_text="Usually 1. Leave empty if the airline doesn't have a "
        "special elite program (e.g., Aegean).", blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    only_elites = models.BooleanField(default=False, verbose_name="Only valid "
        "for elites.")
    other_restrictions = models.TextField(null=True, blank=True)
    fare_name = models.CharField(max_length=100, help_text="The human-readable "
        "name for the fare class, according to the earning airline. E.g., "
        "'Economy class' or 'Business class'.", null=True, blank=True)

    def __unicode__(self):
        return "%s. %d%%, %d" % (self.fare_class, self.base_multiplier,
            self.minimum_miles)
