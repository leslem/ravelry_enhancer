from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Lower

from core.models import TimeStampedModel
from core import utils

# max_lengths: 100 for short names, 1000 for descriptions, none for comments

INCH_TOLERANCE = 0.5

# TODO: set type for each of the terminal models to a default value in custom save method


class StorageLocation(TimeStampedModel):
    description = models.CharField(max_length=None, blank=True)
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(Lower("name"), name="unique_lower_name")]

    def __str__(self) -> str:
        return f"Storage location {self.name}"


# region: Abstract base models


class Tool(TimeStampedModel):
    # TODO: may want to refine type somewhat -- should it be the lowest level?
    class ToolType(models.TextChoices):
        CABLE = "cable", "Cable needle"
        CIRCULAR = "circular", "Fixed circular needle"
        CROCHET = "crochet", "Crochet hook"
        DPN = "dpn", "Double pointed needle"
        INTERCHANGEABLE_CABLE = "interchangeable cable", "Interchangeable cable"
        INTERCHANGEABLE_TIP = "interchangeable tip", "Interchangeable tip"
        STRAIGHT = "straight", "Straight needle"
        SPINDLE = "spindle", "Spindle"
        LOOM = "loom", "Weaving loom"

    type = models.CharField(max_length=100, choices=ToolType.choices)
    brand = models.CharField(max_length=100)
    comment = models.CharField(max_length=None, blank=True)
    date_acquired = models.DateField()
    is_retired = models.BooleanField(default=False)
    material = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # TODO: project = models.ManyToManyField(ravelry.Project)
    quantity = models.IntegerField(
        default=1
    )  # Since I can't distinguish them in real life, only track unique tool types
    source = models.CharField(max_length=1000)
    storage_location = models.ForeignKey(StorageLocation, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True


class CircularCord(models.Model):
    cord_color = models.CharField()
    cord_length_cm = models.FloatField()
    cord_length_in = models.FloatField()
    has_swivel = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Custom save method.

        Automatically sets cord_length_cm from cord_length_in or vice versa.
        """
        # Set cm from in measure given
        if self.cord_length_cm is None and self.cord_length_in is not None:
            self.cord_length_cm = utils.in_to_cm(self.cord_length_in)
        # Set in from cm measure given
        elif self.cord_length_in is None and self.cord_length_cm is not None:
            self.cord_length_in = utils.cm_to_in(self.cord_length_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.cord_length_cm is not None and self.cord_length_in is not None:
            in_diff = abs(utils.cm_to_in(self.cord_length_cm) - self.cord_length_in)
            # cm_diff = abs(utils.in_to_cm(self.cord_length_in) - self.cord_length_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "cord length in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.cord_length_in, "cm_value": self.cord_length_cm},
                )
        # Call the "real" save method.
        super(CircularCord, self).save(*args, **kwargs)


class NeedleTip(models.Model):
    diameter_mm = models.FloatField()
    tip_color = models.CharField()
    tip_length_cm = models.FloatField()
    tip_length_in = models.FloatField()
    us_size = models.CharField()

    class Meta:
        abstract = True

    def size_string(self) -> str:
        return f"{self.diameter_mm} mm (US {self.us_size})"

    def save(self, *args, **kwargs):
        """Custom save method.

        Automatically sets tip_length_cm from tip_length_in or vice versa.
        """
        # Set cm from in measure given
        if self.tip_length_cm is None and self.tip_length_in is not None:
            self.tip_length_cm = utils.in_to_cm(self.tip_length_in)
        # Set in from cm measure given
        elif self.tip_length_in is None and self.tip_length_cm is not None:
            self.tip_length_in = utils.cm_to_in(self.tip_length_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.tip_length_cm is not None and self.tip_length_in is not None:
            in_diff = abs(utils.cm_to_in(self.tip_length_cm) - self.tip_length_in)
            # cm_diff = abs(utils.in_to_cm(self.tip_length_in) - self.tip_length_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "tip length in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.tip_length_in, "cm_value": self.tip_length_cm},
                )
        # Call the "real" save method.
        super(NeedleTip, self).save(*args, **kwargs)


class Interchangeable(models.Model):
    interchangeable_system = models.CharField(max_length=100)

    class Meta:
        abstract = True


class KnittingNeedle(Tool):
    total_length_cm = models.FloatField()
    total_length_in = models.FloatField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Custom save method.

        Automatically sets total_length_cm from total_length_in or vice versa.
        """
        # Set cm from in measure given
        if self.total_length_cm is None and self.total_length_in is not None:
            self.total_length_cm = utils.in_to_cm(self.total_length_in)
        # Set in from cm measure given
        elif self.total_length_in is None and self.total_length_cm is not None:
            self.total_length_in = utils.cm_to_in(self.total_length_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.total_length_cm is not None and self.total_length_in is not None:
            in_diff = abs(utils.cm_to_in(self.total_length_cm) - self.total_length_in)
            # cm_diff = abs(utils.in_to_cm(self.total_length_in) - self.total_length_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "Total length in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.total_length_in, "cm_value": self.total_length_cm},
                )
        # Call the "real" save method.
        super(KnittingNeedle, self).save(*args, **kwargs)


# endregion

# region: Terminal models


class StraightNeedle(KnittingNeedle, NeedleTip):
    # total length is tip length
    set_count = models.IntegerField(default=2)  # Can be 1 if I've lost one

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"), Lower("model"), "total_length_in", "diameter_mm", "us_size", name="unique_straight"
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.size_string(), self.total_length_in, self.tip_color, self.brand, self.model, self.material, ))} straight needles"


class InterchangeableTip(KnittingNeedle, NeedleTip, Interchangeable):
    # total length is tip length

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"),
                Lower("model"),
                "tip_length_in",
                "diameter_mm",
                "us_size",
                "interchangeable_system",
                name="unique_interchangeable_tip",
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.size_string(), self.total_length_in, self.tip_color, self.brand, self.model, self.material, ))} interchangeable needle tips from the {self.interchangeable} system"


class InterchangeableCord(KnittingNeedle, CircularCord, Interchangeable):
    # total length is cord length
    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"),
                Lower("model"),
                "cord_length_in",
                "cord_color",
                "interchangeable_system",
                name="unique_interchangeable_cord",
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.total_length_in, self.cord_color, self.brand, self.model, self.material, ))} interchangeable circular cord from the {self.interchangeable_system} system"


class FixedCircular(KnittingNeedle, NeedleTip, CircularCord):
    # TODO: ensure total length is tip length + cord length

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"),
                Lower("model"),
                "tip_length_in",
                "diameter_mm",
                "us_size",
                "total_length_in",
                name="unique_fixed_circular",
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.size_string(), self.total_length_in, self.tip_color, self.brand, self.model, self.material, ))} fixed circular needle"


class DoublePointedNeedle(KnittingNeedle, NeedleTip):
    # TODO: total length is tip length
    set_count = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"), Lower("model"), "total_length_in", "diameter_mm", "us_size", name="unique_dpn"
            )
        ]

    def __str__(self) -> str:
        return f"Set of {self.set_count} {' '.join((self.size_string(), self.total_length_in, self.tip_color, self.brand, self.model, self.material, ))} double-pointed needles"


class CableNeedle(KnittingNeedle, NeedleTip):
    # TODO: total length is tip length

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"), Lower("model"), "tip_length_in", "diameter_mm", "us_size", name="unique_cable_needle"
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.size_string(), self.total_length_in, self.tip_color, self.brand, self.model, self.material, ))} cable needle"


class CrochetHook(Tool):
    diameter_mm = models.FloatField()
    handle_length_cm = models.FloatField()
    handle_length_in = models.FloatField()
    handle_material = models.CharField()

    class Style(models.TextChoices):
        INLINE = "inline", "Inline"
        TAPERED = "tapered", "Tapered"

    style = models.CharField(max_length=100, choices=Style.choices)
    us_size = models.CharField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"), Lower("model"), "diameter_mm", "us_size", name="unique_crochet_hook"
            )
        ]

    def size_string(self) -> str:
        return f"{self.diameter} mm (US {self.us_size})"

    def __str__(self) -> str:
        return f"{' '.join((self.size_string(), self.color, self.brand, self.model, self.material, ))} crochet hook"

    def save(self, *args, **kwargs):
        """Custom save method.

        Automatically sets handle_length_cm from handle_length_in or vice versa.
        """
        # Set cm from in measure given
        if self.handle_length_cm is None and self.handle_length_in is not None:
            self.handle_length_cm = utils.in_to_cm(self.handle_length_in)
        # Set in from cm measure given
        elif self.handle_length_in is None and self.handle_length_cm is not None:
            self.handle_length_in = utils.cm_to_in(self.handle_length_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.handle_length_cm is not None and self.handle_length_in is not None:
            in_diff = abs(utils.cm_to_in(self.handle_length_cm) - self.handle_length_in)
            # cm_diff = abs(utils.in_to_cm(self.handle_length_in) - self.handle_length_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "handle length in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.handle_length_in, "cm_value": self.handle_length_cm},
                )
        # Call the "real" save method.
        super(CrochetHook, self).save(*args, **kwargs)


class Spindle(Tool):
    total_length_cm = models.FloatField()
    total_length_in = models.FloatField()

    class SpindleType(models.TextChoices):
        DROP = "drop", "Drop spindle"
        SUPPORTED = "supported", "Supported spindle"
        TURKISH = "turkish", "Turkish spindle"

    spindle_type = models.CharField(max_length=100, choices=SpindleType.choices)

    class WhorlPosition(models.TextChoices):
        TOP = "top", "Top"
        BOTTOM = "bottom", "Bottom"
        MIDDLE = "middle", "Middle"
        CONVERTIBLE = "convertible", "Convertible"

    whorl_position = models.CharField(max_length=100, choices=WhorlPosition.choices)

    weight_g = models.FloatField()
    weight_oz = models.FloatField()
    whorl_diameter_cm = models.FloatField()
    whorl_diameter_mm = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower("brand"),
                Lower("model"),
                "spindle_type",
                "whorl_position",
                "weight_oz",
                "whorl_diameter_mm",
                name="unique_spindle",
            )
        ]

    def __str__(self) -> str:
        return f"{' '.join((self.brand, self.model, self.material, self.whorl_position))}-whorl {self.spindle_type} spindle"

    def save(self, *args, **kwargs):
        """Custom save method.

        Automatically sets whorl_diameter_cm from whorl_diameter_mm, total_length_cm from total_length_in,
        and weight_g from weight_oz or vice versa.
        """
        # Set cm from in measure given
        if self.total_length_cm is None and self.total_length_in is not None:
            self.total_length_cm = utils.in_to_cm(self.total_length_in)
        # Set in from cm measure given
        elif self.total_length_in is None and self.total_length_cm is not None:
            self.total_length_in = utils.cm_to_in(self.total_length_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.total_length_cm is not None and self.total_length_in is not None:
            in_diff = abs(utils.cm_to_in(self.total_length_cm) - self.total_length_in)
            # cm_diff = abs(utils.in_to_cm(self.total_length_in) - self.total_length_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "Total length in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.total_length_in, "cm_value": self.total_length_cm},
                )

        # Set cm from in measure given
        if self.whorl_diameter_cm is None and self.whorl_diameter_mm is not None:
            self.whorl_diameter_cm = utils.in_to_cm(self.whorl_diameter_mm)
        # Set in from cm measure given
        elif self.whorl_diameter_mm is None and self.whorl_diameter_cm is not None:
            self.whorl_diameter_mm = utils.cm_to_in(self.whorl_diameter_cm)
        # If both are given, make sure they agree, within tolerance
        elif self.whorl_diameter_cm is not None and self.whorl_diameter_mm is not None:
            in_diff = abs(utils.cm_to_in(self.whorl_diameter_cm) - self.whorl_diameter_mm)
            # cm_diff = abs(utils.in_to_cm(self.whorl_diameter_mm) - self.whorl_diameter_cm)
            if in_diff > INCH_TOLERANCE:
                raise ValidationError(
                    "Whorl diameter in inches %(in_value)s and centimeters %(cm_value)s don't agree",
                    params={"in_value": self.whorl_diameter_mm, "cm_value": self.whorl_diameter_cm},
                )

        # Set g from oz measure given
        if self.weight_g is None and self.weight_oz is not None:
            self.weight_g = utils.oz_to_g(self.weight_oz)
        # Set oz from g measure given
        elif self.weight_oz is None and self.weight_g is not None:
            self.weight_oz = utils.g_to_oz(self.weight_g)
        # If both are given, make sure they agree, within tolerance
        elif self.weight_g is not None and self.weight_oz is not None:
            oz_diff = abs(utils.g_to_oz(self.weight_g) - self.weight_oz)
            # g_diff = abs(utils.oz_to_g(self.weight_oz) - self.weight_g)
            if oz_diff > 0.5:
                raise ValidationError(
                    "Whorl diameter in inches %(oz_value)s and centimeters %(g_value)s don't agree",
                    params={"oz_value": self.weight_oz, "g_value": self.weight_g},
                )

        # Call the "real" save method.
        super(Spindle, self).save(*args, **kwargs)


# TODO: class Loom(Tool):

# endregion
