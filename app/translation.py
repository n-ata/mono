from .models import *
from modeltranslation.translator import register, TranslationOptions


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Genre)
class GenreTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Playlist)
class PlaylistTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Audiobook)
class AudiobookTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'author', )
