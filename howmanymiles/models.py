from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


LOCATION_RESOLUTIONS = (
    (1, 'Region (supernational)'),
    (2, 'Country'),
    (3, 'City'),
    (4, 'Airport'),
)


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

    def get_absolute_url(self):
        return reverse('airline_detail', args=[self.pk])

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

    def get_earning_partners(self):
        """
        i.e., airlines we can earn with if we travel with this airline. Returns
        a tuple containing (allied_partners, other_partners).
        """
        partner_pks = self.operating_rules.values('earning_airline').distinct()
        partner_pks = [d['earning_airline'] for d in partner_pks]
        partners = Airline.objects.filter(pk__in=partner_pks)
        return (partners.filter(alliance=self.alliance),
                partners.exclude(alliance=self.alliance))

    def get_operating_partners(self):
        """
        i.e., airlines we can travel with if we wish to earn with this airline.
        Returns a tuple containing (allied_partners, other_partners).
        """
        partner_pks = self.earning_rules.values('operating_airline').distinct()
        partner_pks = [d['operating_airline'] for d in partner_pks]
        partners = Airline.objects.filter(pk__in=partner_pks)
        return (partners.filter(alliance=self.alliance),
                partners.exclude(alliance=self.alliance))


class EliteBonus(models.Model):
    earning_airline = models.ForeignKey(Airline, related_name='bonuses')
    elite_level = models.CharField(max_length=50)
    bonus_percentage = models.IntegerField(help_text="Based on the number "
        "of miles flown, including minimums.")

    class Meta:
        verbose_name_plural = 'Elite bonuses'


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


class Location(models.Model):
    name = models.CharField(max_length=50)
    resolution = models.IntegerField(choices=LOCATION_RESOLUTIONS)

    def __unicode__(self):
        return self.name


class AccrualRule(models.Model):
    operating_airline = models.ForeignKey(Airline,
        related_name='operating_rules')
    earning_airline = models.ForeignKey(Airline, related_name='earning_rules')
    fare_classes = models.CharField(help_text="The fare classes that this rule "
        "applies to, with no separator. e.g., JCDZ.", max_length=26)
    award_miles_percentage = models.IntegerField()
    tier_miles_percentage = models.IntegerField()
    num_segments = models.DecimalField(max_digits=2, decimal_places=1,
        help_text="Usually 1.", default=1, verbose_name="Segments")
    standard_minimum = models.IntegerField(default=0, help_text="The minimum "
        "number of miles earned by regular (non-elite) members.")
    elite_minimum = models.IntegerField(default=0, help_text="The minimum "
        "number of miles aerned by elite members.")
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    other_restrictions = models.TextField(null=True, blank=True)
    origin = models.ForeignKey(Location, related_name='+', null=True,
        blank=True)
    destination = models.ForeignKey(Location, related_name='+', null=True,
        blank=True)
    fare_name = models.CharField(max_length=100, help_text="The human-readable "
        "name for the fare class, according to the earning airline. E.g., "
        "'Economy class' or 'Business class'.", null=True, blank=True)
