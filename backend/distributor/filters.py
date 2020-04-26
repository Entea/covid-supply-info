from django_filters import Filter, FilterSet
from rest_framework.exceptions import ValidationError

from .models import Distribution


class MultipleListFilter(Filter):
    MAX_LIMIT = 20

    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')

        if len(values) > self.MAX_LIMIT:
            raise ValidationError('Max number of ids should be less than equal 20')

        return super(MultipleListFilter, self).filter(qs, values).distinct()


class DistributionFilter(FilterSet):
    """
    Available filter route /api/v1/distributions/?donation=1,2,3
    """
    donations = MultipleListFilter(field_name='donation')

    class Meta:
        model = Distribution
        fields = ('donations',)
