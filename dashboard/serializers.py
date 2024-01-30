from rest_framework import serializers
from app.models import (
    Artist,
    Song,
    Album
    )
from django.utils.timezone import localtime
from django.contrib.auth.models import Group

base_url = 'https://mono.com.tm'
format_data = "%Y-%m-%d"
format_date_and_time = "%Y-%m-%d %H:%M:%S"

class ArtistsListSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField('_countries')
    updated_by = serializers.SerializerMethodField('_updated_by')
    image = serializers.SerializerMethodField('_image')
    updated_at = serializers.SerializerMethodField('_updated_at')
    
    class Meta:
        model = Artist
        fields = ("id", "name", "image", 'countries', "artist_of_the_week", "updated_by", "updated_at", 'listened_count')
    
    def _countries(self, obj):
        countries = []
        for cntr in obj.countries.all():
            countries.append(cntr.name)
        return countries

    def _updated_by(self, obj):
        return obj.updated_by.phone

    def _image(self, obj):
        return base_url + obj.image.url
    
    def _updated_at(self, obj):
        return obj.updated_at.strftime(format_data)
    
class ArtistSongsListSerializer(serializers.ModelSerializer):
    album = serializers.SerializerMethodField('_album')
    genres = serializers.SerializerMethodField('_genres')
    updated_by = serializers.SerializerMethodField('_updated_by')
    image = serializers.SerializerMethodField('_image')
    audio = serializers.SerializerMethodField('_audio')
    updated_at = serializers.SerializerMethodField('_updated_at')
    
    class Meta:
        model = Song
        fields = ("id", "name", "image", 'listened_count', "hit", "top", "genres", 'album', 'audio', 'order', 'updated_by', 'updated_at')
    
    def _album(self, obj):
        if obj.album_id:
            return obj.album.name
        else:
            return None
    
    def _genres(self, obj):
        genres = []
        for genre in obj.genres.all():
            genres.append(genre.name)
        return genres

    def _updated_by(self, obj):
        return obj.updated_by.phone

    def _image(self, obj):
        if obj.image:
            return base_url + obj.image.url
        return None
    
    def _audio(self, obj):
        return base_url + obj.audio.url
    
    def _updated_at(self, obj):
        return obj.updated_at.strftime(format_data)
    
class ArtistAlbumListSerializer(serializers.ModelSerializer):
    updated_by = serializers.SerializerMethodField('_updated_by')
    image = serializers.SerializerMethodField('_image')
    updated_at = serializers.SerializerMethodField('_updated_at')
    
    class Meta:
        model = Album
        fields = ("id", "name", "image", 'year', "trend", "is_new", "order", 'updated_by', 'updated_at')
    

    def _updated_by(self, obj):
        return obj.updated_by.phone

    def _image(self, obj):
        return base_url + obj.image.url
    
    def _updated_at(self, obj):
        return obj.updated_at.strftime(format_data)
    

class ArtistsSerializer(serializers.ModelSerializer):
    countries = serializers.SerializerMethodField('_countries')
    updated_by = serializers.SerializerMethodField('_updated_by')
    image = serializers.SerializerMethodField('_image')
    updated_at = serializers.SerializerMethodField('_updated_at')
    
    class Meta:
        model = Artist
        fields = ("id", "name", "image", 'countries', "artist_of_the_week", "updated_by", "updated_at", 'listened_count')
    
    def _countries(self, obj):
        countries = []
        for cntr in obj.countries.all():
            countries.append(cntr.id)
        return countries

    def _updated_by(self, obj):
        return obj.updated_by.phone

    def _image(self, obj):
        return base_url + obj.image.url
    
    def _updated_at(self, obj):
        return obj.updated_at.strftime(format_data)
    
class AlbumArtistsListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Artist
        fields = ("id", "name")