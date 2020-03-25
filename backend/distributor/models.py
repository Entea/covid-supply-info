from django.contrib.auth.models import User
from django.db import models

from django.utils.translation import ugettext as _


class NeedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), unique=True)

    def __str__(self):
        return self.name


class Need(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'), null=False, blank=False)
    type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Type'), null=False)
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
        return "%s %s" % (self.name, self.type)
