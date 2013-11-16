from django.contrib import admin

from howmanymiles.models import Alliance, Airline, FareClass, MileageMultiplier


class MileageMultiplierInline(admin.StackedInline):
    model = MileageMultiplier


class FareClassAdmin(admin.ModelAdmin):
    inlines = [MileageMultiplierInline]
    list_display = ('airline', 'class_code')


admin.site.register(Alliance)
admin.site.register(Airline)
admin.site.register(FareClass, FareClassAdmin)
