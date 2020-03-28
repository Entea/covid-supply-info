from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models
from django.core.exceptions import ValidationError

from django.utils.translation import ugettext as _
from django.core.validators import RegexValidator


class Measure(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name (liters, kg, etc.)'), unique=True)

    def __str__(self):
        return self.name


class NeedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT, verbose_name=_('Measure (liters, kg, etc.)'),
                                null=True)
    price_per_piece = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price per piece (KGS)"))
    modified_at = models.DateTimeField(verbose_name=_('Modified Date'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Created Date'), auto_now_add=True, blank=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False)

    def __str__(self):
        return "%s %s" % (self.name, self.measure)

    class Meta:
        verbose_name = _("Need Type")
        verbose_name_plural = _("Need Types")


class Donation(models.Model):
    ORGANIZATION = 'ORGANIZATION'
    PERSON = 'PERSONAL'

    DONATOR_TYPES = (
        (ORGANIZATION, _('ORGANIZATION')),
        (PERSON, _('PERSONAL'))
    )
    donator_type = models.CharField(verbose_name=_('Donator Type'), choices=DONATOR_TYPES, max_length=12,
                                    default=ORGANIZATION)
    donator_name = models.CharField(max_length=200, verbose_name=_('Donator Name'))
    description = models.TextField(verbose_name=_("Donation Description"), max_length=1000)

    modified_at = models.DateTimeField(verbose_name=_('Modified Date'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Created Date'), editable=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False)

    def __str__(self):
        return self.donator_name


class DonationDetail(models.Model):
    need_type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Need Type'))
    amount = models.PositiveSmallIntegerField(verbose_name=_('Amount'))
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT, verbose_name=_('Donation)'),
                                 related_name='details')

    def __str__(self):
        return "{} {}".format(self.need_type, self.amount)


class Region(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Region'))

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return '{} {}'.format(self.name, self.region)


class Locality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('District'))

    class Meta:
        verbose_name = _("Locality")
        verbose_name_plural = _("Locality")

    def __str__(self):
        return '{} {}'.format(self.name, self.district)


class Hospital(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    code = models.CharField(max_length=50, verbose_name=_('Code'))
    address = models.CharField(max_length=500, verbose_name=_('Address'), null=True)
    location = PointField(help_text="To generate the map for your location", null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, verbose_name=_("Locality"), null=True)

    def __str__(self):
        return '{} {}'.format(self.name, self.locality)

    @property
    def full_location(self):
        full_location = dict(longitude=self.location.y, latitude=self.location.x)
        return full_location


class HospitalPhoneNumber(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, verbose_name=_("Hospital"),
                                 related_name='phone_numbers')
    phone_number_regex = RegexValidator(regex='^[0]\d{3,4}[- ]?\d{1,2}[- ]?\d{2}[- ]?\d{2}$',
                                        message="Phone number must be in these formats : 0555123456 or 03134 5 26 71 or 0312 45-26-71")

    value = models.CharField(validators=[phone_number_regex], max_length=30, verbose_name=_('Phone Number'))

    def __str__(self):
        return self.value


class StatisticCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Statistic Category")
        verbose_name_plural = _("Statistic Categories")


class Statistic(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name=_("Hospital"),
                                 related_name='statistics')
    category = models.ForeignKey(StatisticCategory, on_delete=models.CASCADE, verbose_name=_("Category"), null=True)
    actual = models.IntegerField(verbose_name=_('Actual'))
    capacity = models.IntegerField(verbose_name=_('Capacity'), null=True, blank=True)
    has_capacity = models.BooleanField(verbose_name=_("Has Capacity?"), default=False)

    def __str__(self):
        return self.category.name

    @property
    def need_help(self):
        return True if self.has_capacity and self.actual > self.capacity else False


class HelpRequest(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name=_("Locality"), null=True)
    position = models.CharField(max_length=50, verbose_name=_('Position'))
    hospital_name = models.CharField(max_length=250, verbose_name=_('Hospital Name'))
    phone_number = models.CharField(max_length=100, verbose_name=_('Phone Number'))
    description = models.TextField(max_length=500, verbose_name=_('Description'))
    created_at = models.DateTimeField(verbose_name=_('Created Date'), editable=True, auto_now_add=True)
    is_read = models.BooleanField(verbose_name=_("Read"), default=False)
    read_at = models.DateTimeField(verbose_name=_('Read Date'), blank=True, null=True, editable=False)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class HospitalNeeds(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, verbose_name=_("Hospital"), related_name='needs')
    need_type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Need Type'))
    reserve_amount = models.IntegerField(verbose_name=_('Reserve amount'))
    request_amount = models.IntegerField(verbose_name=_('Request amount'))
    created_at = models.DateTimeField(verbose_name=_('Created Date'), auto_now_add=True, blank=True, editable=False)

    def __str__(self):
        return "{} {}".format(self.reserve_amount, self.request_amount)
