from django.db import models

from core.models import TimeStampedModel

# max_lengths: 100 for short names, 1000 for descriptions, none for comments

class StorageLocation(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=None)


class Tool(TimeStampedModel):
    comment = models.CharField(max_length=None)
    storage_location = models.ForeignKey(StorageLocation, null=True, blank=True,
                                         on_delete=models.SET_NULL)
    # TODO: may want to refine this somewhat -- should it be the lowest level?
    class ToolType(models.TextChoices):
        CABLE = "cable", _("Cable needle")
        CIRCULAR = "circular", _("Fixed circular needle")
        CROCHET = "crochet", _("Crochet hook")
        DPN = "dpn", _("Double pointed needle")
        INTERCHANGEABLECABLE = "interchangeable cable", _("Interchangeable cable")
        INTERCHANGEABLETIP = "interchangeable tip", _("Interchangeable tip")
        HOLDER = "holder", _("Stitch holder")
        STRAIGHT = "straight", _("Straight needle")
    type = models.CharField(
        max_length=100,
        choices=ToolType.choices,
    )
    source = models.CharField(max_length=1000)
    # TODO: project = models.ManyToManyField(ravelry.Project)
    date_acquired = models.DateTimeField()
    is_retired = models.BooleanField(default=False)
    material = models.CharField()
    model = models.CharField()
    brand = models.CharField()


class KnittingNeedle(Tool):
    diameter = models.FloatField()
    us_size = models.CharField()
    total_length_in = models.FloatField()
    total_length_cm = models.FloatField()

    tip_color = models.CharField()


class InterchangeableTip(KnittingNeedle):
    interchangeable_system = models.CharField()


class InterchangeableCord(KnittingNeedle):
    # diameter and us_size will be blank
    interchangeable_system = models.CharField()
    cord_color = models.CharField()


class FixedCircular(KnittingNeedle):
    cord_length_in = models.FloatField()
    cord_length_cm = models.FloatField()
    tip_length_in = models.FloatField()
    top_length_cm = models.FloatField()
    cord_color = models.CharField()


class DoublePointed(KnittingNeedle):


class CrochetHook(Tool):
    diameter = models.FloatField()
    us_size = models.CharField()
