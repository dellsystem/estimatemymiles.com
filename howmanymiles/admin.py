from django.contrib import admin

from howmanymiles.models import Alliance, Airline, FareClass, MileageMultiplier


class MileageMultiplierInline(admin.StackedInline):
    model = MileageMultiplier
    extra = 0


class FareClassAdmin(admin.ModelAdmin):
    inlines = [MileageMultiplierInline]
    list_display = ('operating_airline', 'class_code', 'earning_airline')


admin.site.register(Alliance)
admin.site.register(Airline)
admin.site.register(FareClass, FareClassAdmin)
