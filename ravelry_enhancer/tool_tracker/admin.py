"""Customization of the admin interface for the tool_tracker app."""

from django.contrib import admin

from . import models


admin.site.register(models.StraightNeedle)
admin.site.register(models.InterchangeableTip)
admin.site.register(models.InterchangeableCord)
admin.site.register(models.FixedCircular)
admin.site.register(models.DoublePointedNeedle)
admin.site.register(models.CableNeedle)
admin.site.register(models.CrochetHook)
admin.site.register(models.Spindle)
