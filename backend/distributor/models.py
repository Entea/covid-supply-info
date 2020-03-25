from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.db import models

from django.utils.translation import ugettext as _


class Measure(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name (liters, kg, etc.)'), unique=True)

    def __str__(self):
        return self.name


class NeedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), null=False, blank=False)
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT, verbose_name=_('Measure (liters, kg, etc.)'),
                                null=True)
    price_per_piece = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Price per piece (KGS)"),
                                          null=False)
    modified_at = models.DateTimeField(verbose_name=_('Modified Date'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Created Date'), auto_now_add=True, blank=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False)

    def __str__(self):
        return "%s %s" % (self.name, self.measure)


class Donation(models.Model):
    ORGANIZATION = 'ORGANIZATION'
    PERSON = 'PERSONAL'

    DONATOR_TYPES = (
        (ORGANIZATION, _('ORGANIZATION')),
        (PERSON, _('PERSONAL'))
    )
    donator_type = models.CharField(verbose_name=_('Donator Type'), choices=DONATOR_TYPES, max_length=12,
                                    default=ORGANIZATION)
    donator_name = models.CharField(max_length=200, verbose_name=_('Donator Name'), null=False, blank=False)
    description = models.TextField(verbose_name=_("Donation Description"), max_length=1000, blank=False)

    modified_at = models.DateTimeField(verbose_name=_('Modified Date'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Created Date'), blank=False, null=False, editable=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False)
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False)

    def __str__(self):
        return self.donator_name


class DonationDetail(models.Model):
    need_type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Need Type'))
    amount = models.PositiveSmallIntegerField(verbose_name=_('Amount'))
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT, verbose_name=_('Donation)'), null=False)

    def __str__(self):
        return "{} {}".format(self.need_type, self.amount)


class Hospital(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), null=False, blank=False)
    code = models.CharField(max_length=50, verbose_name=_('Code'), null=False, blank=False)
    phone_number = models.CharField(max_length=20, verbose_name=_('Phone Number'), null=False, blank=False)
    location = PointField(help_text="To generate the map for your location")

    def __str__(self):
        return self.name
