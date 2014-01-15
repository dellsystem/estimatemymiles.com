from django.contrib import admin

from howmanymiles.models import *


class EliteBonusAdmin(admin.ModelAdmin):
    list_display = ('elite_level', 'earning_airline', 'bonus_percentage')


class AccrualRuleAdmin(admin.ModelAdmin):
    list_display = ('fare_name', 'fare_classes', 'operating_airline',
        'earning_airline', 'start_date', 'end_date', 'origin', 'destination')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'resolution')


admin.site.register(Alliance)
admin.site.register(Airline)
admin.site.register(EliteBonus, EliteBonusAdmin)
admin.site.register(MileageInfoSource)
admin.site.register(Location, LocationAdmin)
admin.site.register(AccrualRule, AccrualRuleAdmin)
