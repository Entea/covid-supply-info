from django_filters import Filter, FilterSet

from .models import Distribution


class MultipleListFilter(Filter):
    def filter(self, qs, value):
        if not value:
            return qs

        self.lookup_expr = 'in'
        values = value.split(',')
        return super(MultipleListFilter, self).filter(qs, values).distinct()


class DistributionFilter(FilterSet):
    """
    Available filter route /api/v1/distributions/?hospitals=1,2,3
    """
    hospitals = MultipleListFilter(field_name='hospital')

    class Meta:
        model = Distribution
        fields = ('hospitals',)
