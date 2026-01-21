from .models import (City, Property, Rules)
from modeltranslation.translator import TranslationOptions,register

@register(City)
class ProductTranslationOptions(TranslationOptions):
    fields = ('city_name',)

@register(Property)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title','descriptions')

@register(Rules)
class ProductTranslationOptions(TranslationOptions):
    fields = ('rules_name',)