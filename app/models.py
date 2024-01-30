from django.db import models
from django.utils.timezone import utc
from django.contrib.auth.models import  AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils.translation import gettext_lazy as _


class Region(models.Model):
    name = models.CharField(max_length=100)
    order = models.IntegerField(default=1)
        
class User(AbstractBaseUser, PermissionsMixin):
    GENDER = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    gender = models.CharField(max_length=10, choices=GENDER, default="male")
    phone = models.CharField(max_length=8, unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    birth_day = models.DateField(auto_now_add=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    otp_code = models.IntegerField(blank=True)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Unselect this instead of deleting accounts.',
    )

    logged_in_first_time = models.BooleanField(default=False)

    invited_by = models.CharField(max_length=100, default='', blank=True)
    invitation_id = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '001. User'
        verbose_name_plural = '001. Users'
        
class MyBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))
    updated_by = models.ForeignKey(
        User,
        blank=True, null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True
class OtpModel(MyBaseModel):
    phone = models.CharField(unique=True, max_length=8)
    otp_code = models.IntegerField(blank=True)
    sended = models.BooleanField(default=False)

    class Meta:
        verbose_name = '002. OTP Models'
        verbose_name_plural = '002. OTP Models'

    def __str__(self):
        return self.phone
    

class Country(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="images/countries",
        default='',
        blank=False, null=False,
    )
    
    class Meta:
        verbose_name = '003. Countries'
        verbose_name_plural = '003. Countries'

    def __str__(self):
        return self.name
    
class Artist(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to="images/artists/%Y/%m/%d",
        default='',
        blank=False, null=False,
    )
    
    artist_of_the_week = models.BooleanField(default=False)
    listened_count = models.IntegerField(default=0)
    countries = models.ManyToManyField(
        Country,
        related_name="artists",
    )

    class Meta:
        verbose_name = '010. Artists'
        verbose_name_plural = '010. Artists'

    def __str__(self):
        return self.name
    
class Album(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/albums/%Y/%m/%d')

    year = models.IntegerField(default=2023)
    trend = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    order = models.IntegerField(default=1)

    class Meta:
        verbose_name = '015. Albums'
        verbose_name_plural = '015. Albums'

    def __str__(self):
        return self.name
    
class Album_Artists(MyBaseModel):
    artist = models.ForeignKey(
        to=Artist, 
        on_delete=models.CASCADE,
        related_name='albums',
        related_query_name='albums')
    album = models.ForeignKey(
        to=Album, 
        on_delete=models.CASCADE,
        related_name='artists',
        related_query_name='artists')
    order = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('artist', 'album')
        verbose_name = '017. Artist Albums'
        verbose_name_plural = '017. Artist Albums'

    
class Genre(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/genres/%Y/%m/%d')
    
    class Meta:
        verbose_name = '020. Genres'
        verbose_name_plural = '020. Genres'

    def __str__(self):
        return self.name
    
class Song(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/songs/%Y/%m/%d', blank=True, null=True)
    listened_count = models.IntegerField(verbose_name='Listened count', default=0)
    hit = models.BooleanField(default=False)
    top = models.BooleanField(default=False)
    year = models.IntegerField(default=0)
    genres = models.ManyToManyField(
        Genre,
        related_name="songs"
    )
    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        related_name="songs",
        blank=True, null=True,
    )
    audio = models.FileField(upload_to="audio/songs/%Y/%m/%d/%H/%M")
    order = models.IntegerField(default=1)

    class Meta:
        verbose_name = '025. Songs'
        verbose_name_plural = '025. Songs'

    def __str__(self):
        return self.name
    
class Song_Artists(MyBaseModel):
    song = models.ForeignKey(
        to=Song, 
        on_delete=models.CASCADE,
        related_name='artists',
        related_query_name='artists')
    artist = models.ForeignKey(
        to=Artist, 
        on_delete=models.CASCADE,
        related_name='songs',
        related_query_name='songs')
    order = models.IntegerField(default=1)  # Field to store the artist's order

    class Meta:
        unique_together = ('song', 'artist')
        verbose_name = '030. Artists Songs'
        verbose_name_plural = '030. Artists Songs'

class PlaylistCategory(MyBaseModel):
    name = models.CharField(max_length=200)
    abbre = models.CharField(max_length=10)
    order = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = '035. PlaylistCategory'
        verbose_name_plural = '035. PlaylistCategory'

    def __str__(self):
        return self.name
    
class Playlist(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='images/playlist/%Y/%m/%d')
    
    order = models.IntegerField(default=1)
    category = models.ForeignKey(
        PlaylistCategory,
        on_delete=models.SET_NULL,
        related_name='playlists',
        related_query_name='playlists',
        blank=True, null=True
    )

    class Meta:
        verbose_name = '040. Playlist'
        verbose_name_plural = '040. Playlist'

    def __str__(self):
        return self.name
    
class Playlist_Songs(MyBaseModel):
    song = models.ForeignKey(
        to=Song, 
        on_delete=models.CASCADE,
        related_name='playlists',
        related_query_name='playlists')
    playlist = models.ForeignKey(
        to=Playlist, 
        on_delete=models.CASCADE,
        related_name='songs',
        related_query_name='songs')
    order = models.IntegerField(default=1)  # Field to store the artist's order

    class Meta:
        unique_together = ('song', 'playlist')
        verbose_name = '042. Playlist Songs'
        verbose_name_plural = '042. Playlist Songs'
    
class Audiobook(MyBaseModel):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/audiobooks/%Y/%m/%d')
    description = models.TextField()
    author = models.CharField(max_length=200)
    audio = models.FileField(
        upload_to="audio/books/%Y/%m/%d",
        blank=True, null=True,
    )

    class Meta:
        verbose_name = '045. Audiobook'
        verbose_name_plural = '045. Audiobook'

    def __str__(self):
        return self.name