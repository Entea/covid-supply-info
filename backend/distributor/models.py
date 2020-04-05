from cacheops import cached
from django.contrib.auth.models import User
from django.contrib.gis.db.models import PointField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import Sum
from django.utils.translation import ugettext as _

from distributor.constants import DISTRIBUTION_STATUSES

DEFAULT_INDICATOR = -1


class Measure(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование (литры, килограммы, и др.)'), unique=True,
                            help_text=_('Введите наименование, например литр'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Единица измерения')
        verbose_name_plural = _('Единицы измерений')


class NeedType(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text=_('Введите наименование'))
    measure = models.ForeignKey(Measure, on_delete=models.PROTECT, verbose_name=_('Расширение'),
                                null=True, help_text=_('Выберите единицу измерения'))
    modified_at = models.DateTimeField(verbose_name=_('Дата изменения'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True, blank=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False, help_text=_('Было создано пользователем'),
                                   verbose_name=_('Было создано'))
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False, help_text=_('Было изменено пользователем'),
                                    verbose_name=_('Было изменено'))

    def __str__(self):
        return "%s %s" % (self.name, self.measure)

    class Meta:
        verbose_name = _('Тип потребности')
        verbose_name_plural = _('Типы потребностей')


class Donation(models.Model):
    ORGANIZATION = 'ORGANIZATION'
    PERSON = 'PERSONAL'
    DONOR = 'DONOR'

    DONATOR_TYPES = (
        (ORGANIZATION, _('ORGANIZATION')),
        (PERSON, _('PERSONAL')),
        (DONOR, _('DONOR')),
    )
    donator_type = models.CharField(verbose_name=_('Тип пожертвования'), choices=DONATOR_TYPES, max_length=12,
                                    default=ORGANIZATION, help_text=_('Выберите тип пожертвования'))
    donator_name = models.CharField(max_length=200, verbose_name=_('Имя мецената'), help_text=_('Введите имя мецената'))
    description = models.TextField(max_length=1000, verbose_name=_("Описание пожертвования"),
                                   help_text=_('Введите описание пожертвования'))

    modified_at = models.DateTimeField(verbose_name=_('Дата изменения'), auto_now=True, null=True, blank=True,
                                       editable=False)
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), editable=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_created_by',
                                   auto_created=True, editable=False, help_text=_('Было создано пользователем'),
                                   verbose_name=_('Было создано'))
    modified_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='%(class)s_modified_by',
                                    auto_created=True, editable=False, help_text=_('Было изменено пользователем'),
                                    verbose_name=_('Было изменено'))

    class Meta:
        verbose_name_plural = _('Пожертвования')
        verbose_name = _('Пожертвование')

    def __str__(self):
        return self.donator_name


class DonationDetail(models.Model):
    need_type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Тип нужды'),
                                  help_text=_('Выберите тип нужды'))
    amount = models.PositiveIntegerField(verbose_name=_('Количество'), help_text=_('Введите количество'))
    donation = models.ForeignKey(Donation, on_delete=models.PROTECT, verbose_name=_('Пожертвование)'),
                                 related_name='details', help_text=_('Выберите ранее созданное пожертвование'))
    price_per_piece = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_("Цена за одну единицу (KGS)"),
                                          help_text=_('Цена в сомах'))

    class Meta:
        verbose_name_plural = _('Детали пожертвований')
        verbose_name = _('Детали пожертвования')

    def __str__(self):
        return "{} {}".format(self.need_type, self.amount)


class Region(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text=_('Введите название региона'))

    class Meta:
        verbose_name = _("Область/город")
        verbose_name_plural = _("Области/города")

    def __str__(self):
        return self.name


class District(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text=_('Введите название района'))
    region = models.ForeignKey(Region, on_delete=models.CASCADE, verbose_name=_('Регион'),
                               help_text=_('Выберите ранее созданный регион'))

    class Meta:
        verbose_name = _("Район")
        verbose_name_plural = _("Районы")

    @cached(timeout=36_000)
    def __str__(self):
        return '{} {}'.format(self.name, self.region)


class Locality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text=_('Введите наименование'))
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name=_('Район'),
                                 help_text=_('Выберите район'))

    class Meta:
        verbose_name = _("Местность")
        verbose_name_plural = _("Местности")

    @cached(timeout=36_000)
    def __str__(self):
        return '{} {}'.format(self.name, self.district)


class Hospital(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), help_text=_('Введите название больницы'))
    code = models.CharField(max_length=50, verbose_name=_('Код'), help_text=_('Введите код'), unique=True)
    address = models.CharField(max_length=500, verbose_name=_('Адрес'), null=True, help_text=_('Введите адрес'))
    location = PointField(help_text="Для создания местоположения", null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE, verbose_name=_("Местоположение"), null=True)

    class Meta:
        verbose_name_plural = _('Больницы')
        verbose_name = _('Больница')

    search_locality_id = models.IntegerField(null=True, verbose_name=_("Search Locality ID"))
    search_district_id = models.IntegerField(null=True, verbose_name=_("Search District ID"))
    search_region_id = models.IntegerField(null=True, verbose_name=_("Search Region ID"))

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.locality:
            self.search_locality_id = self.locality.pk
            if self.locality.district:
                self.search_district_id = self.locality.district.pk
                if self.locality.district.region:
                    self.search_region_id = self.locality.district.region.pk

        super(Hospital, self).save_base(force_insert=force_insert, force_update=force_update, using=using,
                                        update_fields=update_fields)

    def __str__(self):
        return '{} {}'.format(self.name, self.locality)

    @property
    def full_location(self):
        full_location = dict(
            lat=None if not self.location or not self.location.y else self.location.y,
            lng=None if not self.location or not self.location.x else self.location.x
        )
        return full_location

    @property
    def indicator(self):
        stat = self.needs.aggregate(total_request=Sum('request_amount'),
                                    total_reserve=Sum('reserve_amount'))

        ttl_request = stat['total_request']
        ttl_reserve = stat['total_reserve']

        return DEFAULT_INDICATOR if not ttl_request or not ttl_reserve else int(round(ttl_reserve * 100 / ttl_request))


class HospitalPhoneNumber(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, verbose_name=_("Больница"),
                                 related_name='phone_numbers')
    phone_number_regex = RegexValidator(regex='^[0]\d{3,4}[- ]?\d{1,2}[- ]?\d{2}[- ]?\d{2}$',
                                        message="Телефонный номер должен быть : 0555123456 или 03134 5 26 71 или 0312 45-26-71")

    value = models.CharField(validators=[phone_number_regex], max_length=30, verbose_name=_('Телефонный номер'))

    class Meta:
        verbose_name_plural = _('Телефонные номера больниц')
        verbose_name = _('Телефонный номер больницы')

    def __str__(self):
        return self.value


class StatisticCategory(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'), unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Категория статистики")
        verbose_name_plural = _("Категории статистик")


class Statistic(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, verbose_name=_("Больница"),
                                 related_name='statistics')
    category = models.ForeignKey(StatisticCategory, on_delete=models.CASCADE, verbose_name=_("Категория"), null=True)
    actual = models.IntegerField(verbose_name=_('Текущий показатель'))
    capacity = models.IntegerField(verbose_name=_('Требуемое количество'), null=True, blank=True)
    has_capacity = models.BooleanField(verbose_name=_('Показывать поле "Требуемое количество" '), default=False,
                                       help_text=_('Отметьте галочкой чтобы показать поле'))

    class Meta:
        verbose_name_plural = _('Статистики')
        verbose_name = _('Статистика')

    def __str__(self):
        return self.category.name

    @property
    def need_help(self):
        return True if self.has_capacity and self.actual > self.capacity else False


class HelpRequest(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('Имя'))
    last_name = models.CharField(max_length=50, verbose_name=_('Фамилия'))
    locality = models.ForeignKey(Locality, on_delete=models.PROTECT, verbose_name=_("Местоположение"), null=True)
    position = models.CharField(max_length=50, verbose_name=_('Позиция'))
    hospital_name = models.CharField(max_length=250, verbose_name=_('Наименование больницы'))
    phone_number = models.CharField(max_length=100, verbose_name=_('Телефонный номер'))
    description = models.TextField(max_length=500, verbose_name=_('Описание'))
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), editable=True, auto_now_add=True)
    is_read = models.BooleanField(verbose_name=_("Обработано"), default=False)
    read_at = models.DateTimeField(verbose_name=_('Дата обработки'), blank=True, null=True, editable=False)

    class Meta:
        verbose_name_plural = _('Заявки')
        verbose_name = _('Заявка')

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class HospitalNeeds(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.PROTECT, verbose_name=_("Больница"), related_name='needs')
    need_type = models.ForeignKey(NeedType, on_delete=models.PROTECT, verbose_name=_('Тип нужды'))
    reserve_amount = models.IntegerField(verbose_name=_('В наличии'))
    request_amount = models.IntegerField(verbose_name=_('Требуемое количество'))
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = _('Потребности больниц')
        verbose_name = _('Потребность')

    def __str__(self):
        return "{} {}".format(self.reserve_amount, self.request_amount)


class Page(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Наименование'))
    url = models.CharField(max_length=200, verbose_name=_('Ссылка'))
    content = models.TextField(max_length=1000, verbose_name=_('Контент'))

    class Meta:
        verbose_name = _("Страница")
        verbose_name_plural = _("Страницы")

    def __str__(self):
        return '{} /{}'.format(self.name, self.url)


class ContactInfo(models.Model):
    text = models.CharField(max_length=300, verbose_name=_('Текст'))

    def save(self, *args, **kwargs):
        if not self.pk and ContactInfo.objects.exists():
            raise ValidationError('Контактная информация уже существует')
        return super(ContactInfo, self).save(*args, **kwargs)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = _('Контактная информация')
        verbose_name = _('Контактная информация')


class ContactInfoPhoneNumber(models.Model):
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.PROTECT, verbose_name=_("Контактная информация"),
                                     related_name='phone_numbers')
    phone_number_regex = RegexValidator(regex=r'^[0]\d{3,4}[- ]?\d{1,2}[- ]?\d{2}[- ]?\d{2}$',
                                        message="Телефонный номер должен быть: 0555123456, 03134 5 26 71, 0312 45-26-71")

    value = models.CharField(validators=[phone_number_regex], max_length=30, verbose_name=_('Телефонный номер'))

    is_whats_app = models.BooleanField(verbose_name=_("Вотсап номер?"), default=False)

    class Meta:
        verbose_name_plural = _('Телефонные номера')
        verbose_name = _('Телефонный номер')

    def __str__(self):
        return self.value


class ContactInfoEmail(models.Model):
    contact_info = models.ForeignKey(ContactInfo, on_delete=models.PROTECT, verbose_name=_("Контактная информация"),
                                     related_name='emails')
    value = models.EmailField(max_length=100, verbose_name=_('Электронный адрес'))

    class Meta:
        verbose_name_plural = _('Электронные адреса')
        verbose_name = _('Электронный адрес')

    def __str__(self):
        return self.value


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=200, verbose_name=_('ФИО'))
    phone_number = models.CharField(max_length=200, verbose_name=_('Телефон'), null=True)
    email = models.EmailField(max_length=200, verbose_name=_('Электронный адрес'), null=True)
    title = models.CharField(max_length=100, verbose_name=_('Тема сообщения'))
    body = models.TextField(max_length=400, verbose_name=_('Сообщение'))
    created_at = models.DateTimeField(verbose_name=_('Дата создания'), auto_now_add=True, blank=True, editable=False)

    class Meta:
        verbose_name_plural = _('Сообщения')
        verbose_name = _('Сообщение')

    def __str__(self):
        return self.title


class Distribution(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='distributions')
    sender = models.TextField(verbose_name='Кто выдал?')
    receiver = models.TextField(verbose_name='Кто принял?')
    date_of_distribute = models.DateField(verbose_name='Дата распределения')
    status = models.CharField(max_length=20, choices=DISTRIBUTION_STATUSES, verbose_name='Статус')
    donations = models.ManyToManyField(Donation, verbose_name='Пожертвования')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Распределения'
        verbose_name = 'Запись для распределения'

    def __str__(self):
        return self.hospital.name
