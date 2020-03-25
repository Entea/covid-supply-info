from modeltranslation.translator import translator, TranslationOptions
from .models import Measure, NeedType, Donation, Hospital

class MeasureTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Measure, MeasureTranslationOptions)

class NeedTypeTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(NeedType, NeedTypeTranslationOptions)

class DonationTranslationOptions(TranslationOptions):
    fields = ('description', 'donator_name')

translator.register(Donation, DonationTranslationOptions)

class HospitalTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Hospital, HospitalTranslationOptions)