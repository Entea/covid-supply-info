from django.utils.translation import ugettext as _

READY_TO_SEND = 'ready_to_sent'
SENT = 'sent'
DELIVERED = 'delivered'

DISTRIBUTION_STATUSES = (
    (READY_TO_SEND, _('Подготовлено')),
    (SENT, _('Отправлено')),
    (DELIVERED, _('Доставлено')),
)

ORGANIZATION = 'ORGANIZATION'
PERSON = 'PERSONAL'
DONOR = 'DONOR'
GOVERNMENT = 'GOVERNMENT'

DONATOR_TYPES = (
    (ORGANIZATION, _('ORGANIZATION')),
    (PERSON, _('PERSONAL')),
    (DONOR, _('DONOR')),
    (GOVERNMENT, _('GOVERNMENT')),
)