import decimal
import random
from rest_framework.views import APIView
from django.utils.timezone import localtime
import datetime
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse, JsonResponse
from rest_framework import generics, status
from django.db.models import Prefetch
from django.shortcuts import render
from django.core.paginator import Paginator
from .serializers import *
from .pagination import *
from rest_framework.decorators import api_view, action, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,
)
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .decorators import group_required, ModeratorOnly, SuperUserOnly, OperatorOnly, MarketingOnly
import re
import pytz
from django.utils import timezone
from app.models import (
    Artist,
    Song,
    Country,
    Song,
    Song_Artists,
    Album,
    Album_Artists,
    Genre)
import subprocess

# start uc products
@user_passes_test(lambda u: u.is_superuser)
def artists(request):
    payload = {}
    return render(request, './dashboard/artists/artists.html', context=payload)


class ArtistsListView(generics.ListAPIView):
    serializer_class = ArtistsListSerializer
    queryset =  Artist.objects.order_by('-id').all()
    pagination_class = CustomLimitOffsetPagination
    permission_classes = [SuperUserOnly]

    def get(self, request, *args, **kwargs):
        search = request.GET.get("search[value]", None)
        queryset = self.filter_queryset(self.get_queryset())
        
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": self.request})
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)
    
@user_passes_test(lambda u: u.is_superuser)
def create_artist(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            countries_str = request.POST.getlist('countries', None)
            artist_of_the_week = request.POST.get('artist_of_the_week', False) == 'true'

            banner = request.FILES.get("croppedImage", None)
            print(countries_str)
            countries = [int(c) for c in countries_str]
            
            if len(countries) == 0:
                return JsonResponse({"message": "Yurt sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            now = datetime.datetime.now()
            artist = Artist()
            artist.name = name
            artist.artist_of_the_week = artist_of_the_week
            artist.image = banner
            artist.updated_by = request.user
            artist.save()
            artist.countries.set(countries)
            return JsonResponse({"artist": artist.id}, status=status.HTTP_200_OK)
                
        else:
            countries = Country.objects.all()
            payload = {
                "countries": countries
            }
            return render(request, './dashboard/artists/create-artist.html', context=payload)
    except:
        return JsonResponse({"message": "Yurt sayladynmy?"}, status=status.HTTP_409_CONFLICT)

@user_passes_test(lambda u: u.is_superuser)
def edit_artist(request, id):
    try:
        if request.method == 'POST':
            name = request.POST.get('name', None)
            countries_str = request.POST.getlist('countries', None)
            artist_of_the_week = request.POST.get('artist_of_the_week', False) == 'true'
            is_image_edited = request.POST.get('is_image_edited', False) == 'true'

            banner = request.FILES.get("croppedImage", None)
            countries = [int(c) for c in countries_str]
            
            if len(countries) == 0:
                return JsonResponse({"message": "Yurt sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            
            artist = Artist.objects.get(id=id)
            artist.name = name
            artist.artist_of_the_week = artist_of_the_week
            if is_image_edited:
                artist.image = banner
            
            artist.updated_by = request.user
            artist.save()
            artist.countries.set(countries)
            return JsonResponse({"artist": artist.id}, status=status.HTTP_200_OK)
                
        else:
            countries = Country.objects.all()
            artist = Artist.objects.get(id=id)
            artist = ArtistsSerializer(artist).data
            payload = {
                "countries": countries,
                "artist": artist
            }
            return render(request, './dashboard/artists/edit-artist.html', context=payload)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Yurt sayladynmy?"}, status=status.HTTP_409_CONFLICT)

@user_passes_test(lambda u: u.is_superuser)
@api_view(['GET'])
def artist_details(request, id):
    artist = Artist.objects.get(id=id)
    artist = ArtistsSerializer(artist).data
    top_songs = Song.objects.filter(top=True, artists__artist_id=id).order_by('-id').all()
    top_songs = ArtistSongsListSerializer(top_songs, many=True).data
    albums = Album.objects.filter(artists__artist_id=id).all()
    albums = ArtistAlbumListSerializer(albums, many=True).data
    payload = {
        'artist': artist,
        'top_songs': top_songs,
        'albums': albums
    }
    return render(request, './dashboard/artists/artist-details.html', context=payload)


    


@user_passes_test(lambda u: u.is_superuser)
def delete_artists(request):
    if request.method == 'POST':
        artist_ids_str = request.POST.getlist('artist_ids', None)
        artist_ids = [int(id) for id in artist_ids_str]
        
        try:
            Artist.objects.filter(id__in=artist_ids).delete()
            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@user_passes_test(lambda u: u.is_superuser)
def delete_albums(request):
    if request.method == 'POST':
        album_ids_str = request.POST.getlist('album_ids', None)
        album_ids = [int(id) for id in album_ids_str]
        
        try:
            Album.objects.filter(id__in=album_ids).delete()
            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@user_passes_test(lambda u: u.is_superuser)
def delete_songs(request):
    if request.method == 'POST':
        song_ids_str = request.POST.getlist('song_ids', None)
        song_ids = [int(id) for id in song_ids_str]
        
        try:
            Song.objects.filter(id__in=song_ids).delete()
            return JsonResponse({}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return JsonResponse({}, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

class ArtistSongsListView(generics.ListAPIView):
    serializer_class = ArtistSongsListSerializer
    queryset =  Song.objects.prefetch_related('genres').order_by('-id').all()
    pagination_class = CustomLimitOffsetPagination
    permission_classes = [SuperUserOnly]

    def get(self, request, id, *args, **kwargs):
        search = request.GET.get("search[value]", None)
        queryset = self.filter_queryset(self.get_queryset())
        
        queryset = queryset.filter(artists__artist_id=id)
        
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": self.request})
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

class AlbumSongsListView(generics.ListAPIView):
    serializer_class = ArtistSongsListSerializer
    queryset =  Song.objects.prefetch_related('genres').order_by('-id').all()
    pagination_class = CustomLimitOffsetPagination
    permission_classes = [SuperUserOnly]

    def get(self, request, id, *args, **kwargs):
        search = request.GET.get("search[value]", None)
        queryset = self.filter_queryset(self.get_queryset())
        
        queryset = queryset.filter(album_id=id)
        
        if search:
            queryset = queryset.filter(Q(name__icontains=search))
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={"request": self.request})
            result = self.get_paginated_response(serializer.data)
            data = result.data  # pagination data
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data

        return Response(data, status=status.HTTP_200_OK)
    
@user_passes_test(lambda u: u.is_superuser)
def create_album(request, artist_id, album_id):
    try:
        user=request.user
        if request.method == 'POST':
            name = request.POST.get('name', None)
            year = request.POST.get('year', None)
            order = request.POST.get('order', 0)
            artists_str = request.POST.getlist('artists', None)
            is_new = request.POST.get('is_new', False) == 'true'
            trend = request.POST.get('trend', False) == 'true'
            is_image_edited = request.POST.get('is_image_edited', False) == 'true'
            
            banner = request.FILES.get("croppedImage", None)
            
            artists = [int(c) for c in artists_str]
            
            if len(artists) == 0:
                return JsonResponse({"message": "Artist sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            now = datetime.datetime.now()
            if album_id > 0:
                album = Album.objects.get(id=album_id)
                Album_Artists.objects.filter(album_id=album_id).delete()
                
            else:
                album = Album()
                if not banner:
                    return JsonResponse({"message": "Surat sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            album.name = name
            album.year = year
            if is_image_edited and banner:
                album.image = banner
            album.updated_by = user
            if order:
                album.order = order
            album.is_new = is_new
            album.trend = trend
            album.save()
            album_artsits = []
            
            for i, a_id in enumerate(artists):
                album_artsits.append(Album_Artists(album_id=album.id, artist_id=a_id, order=i, updated_by=user))
            Album_Artists.objects.bulk_create(album_artsits)
            return JsonResponse({"artist": album.id}, status=status.HTTP_200_OK)
                
        else:
            countries = Country.objects.all()
            artists = Artist.objects.get(id=artist_id)
            
            album = None
            if album_id > 0:
                album = Album.objects.prefetch_related('artists').get(id=album_id)
                artists = album.artists.order_by('order')
            
            payload = {
                "countries": countries,
                "artists": artists,
                "album_id": album_id,
                "album": album,
                "artist_id": artist_id
            }
            return render(request, './dashboard/artists/create-album.html', context=payload)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Artist, Surat, Yyl sayladynmy?"}, status=status.HTTP_409_CONFLICT)
    
@user_passes_test(lambda u: u.is_superuser)
def create_album_song(request, artist_id, album_id, song_id):
    try:
        user=request.user
        if request.method == 'POST':
            name = request.POST.get('name', None)
            listened_count = request.POST.get('listened_count', 0)
            order = request.POST.get('order', 0)
            artists_str = request.POST.getlist('artists', None)
            genres_str = request.POST.getlist('genres', None)
            hit = request.POST.get('hit', False) == 'true'
            top = request.POST.get('top', False) == 'true'
            
            audio = request.FILES.get("audio", None)
            
            artists = [int(c) for c in artists_str]
            genres = [int(c) for c in genres_str]
            
            if len(artists) == 0:
                return JsonResponse({"message": "Artist sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            if len(genres) == 0:
                return JsonResponse({"message": "Genre sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            try:
                order = int(order)
            except:
                order = None
            try: 
                listened_count = int(listened_count)
            except:
                listened_count = None
        
            
            if song_id > 0:
                song = Song.objects.get(id=song_id)
                Song_Artists.objects.filter(song_id=song_id).delete()
                
            else:
                song = Song()
                if not audio and song_id == 0:
                    return JsonResponse({"message": "Audio sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            song.name = name
            if listened_count:
                song.listened_count = listened_count
            song.updated_by = user
            if order:
                song.order = order
            song.hit = hit
            if album_id > 0:
                song.album_id = album_id
            song.top = top
            if audio:
                song.audio = audio
            song.save()
            song.genres.set(genres)
            
            song_artsits = []
            
            for i, a_id in enumerate(artists):
                song_artsits.append(Song_Artists(song_id=song.id, artist_id=a_id, order=i, updated_by=user))
            
            Song_Artists.objects.bulk_create(song_artsits)
            if audio:
                location  = song.audio.path
                command = 'ffmpeg -i '+location+' -c:a aac -b:a 128k -vn -hls_time 10 -hls_list_size 0 '+location.replace('.mp3', '')+'.m3u8'
                command = command.split()
                cmd2 = subprocess.Popen(command, stdout=subprocess.PIPE)
                cmd2.wait()
            return JsonResponse({}, status=status.HTTP_200_OK)
                
        else:
            artists = Artist.objects.get(id=artist_id)
            genres = Genre.objects.order_by('name').all()
            
            
            album = None
            if album_id > 0:
                album = Album.objects.prefetch_related('artists').get(id=album_id)
                
            song = None
            song_genres = []
            if song_id > 0:
                song = Song.objects.get(id=song_id)
                song_genres = list(song.genres.order_by('name').values('id'))
                song_genres = [i['id'] for i in song_genres]
                artists = song.artists.order_by('order')
            
            payload = {
                "artists": artists,
                "album_id": album_id,
                "album": album,
                "artist_id": artist_id,
                "genres": genres,
                "song_id": song_id,
                "song": song,
                "song_genres": song_genres
            }
            return render(request, './dashboard/artists/create-album-song.html', context=payload)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Artist, Surat, Yyl sayladynmy?"}, status=status.HTTP_409_CONFLICT)
    
@user_passes_test(lambda u: u.is_superuser)
def create_song(request, artist_id, song_id):
    try:
        user=request.user
        if request.method == 'POST':
            name = request.POST.get('name', None)
            listened_count = request.POST.get('listened_count', 0)
            order = request.POST.get('order', 0)
            artists_str = request.POST.getlist('artists', None)
            genres_str = request.POST.getlist('genres', None)
            hit = request.POST.get('hit', False) == 'true'
            top = request.POST.get('top', False) == 'true'
            album_id = request.POST.get('album', None)
            year = request.POST.get('year', 0)
            
            audio = request.FILES.get("audio", None)
            banner = request.FILES.get("croppedImage", None)
            
            artists = [int(c) for c in artists_str]
            genres = [int(c) for c in genres_str]
            
            if len(artists) == 0:
                return JsonResponse({"message": "Artist sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            if len(genres) == 0:
                return JsonResponse({"message": "Genre sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            
            try:
                order = int(order)
            except:
                order = None
            try: 
                listened_count = int(listened_count)
            except:
                listened_count = None
        
            
            if song_id > 0:
                song = Song.objects.get(id=song_id)
                Song_Artists.objects.filter(song_id=song_id).delete()
                
            else:
                song = Song()
                if not audio and song_id == 0:
                    return JsonResponse({"message": "Audio sayladynmy?"}, status=status.HTTP_409_CONFLICT)
                if not banner:
                    return JsonResponse({"message": "Surat sayladynmy?"}, status=status.HTTP_409_CONFLICT)
            song.name = name
            if listened_count:
                song.listened_count = listened_count
            song.updated_by = user
            if order:
                song.order = order
            if banner:
                song.image=banner
            if album_id:
                song.album_id = album_id
            if year:
                song.year = year
            song.hit = hit
            song.top = top
            if audio:
                song.audio = audio
            song.save()
            song.genres.set(genres)
            
            song_artsits = []
            
            for i, a_id in enumerate(artists):
                song_artsits.append(Song_Artists(song_id=song.id, artist_id=a_id, order=i, updated_by=user))
            
            Song_Artists.objects.bulk_create(song_artsits)
            if audio:
                location  = song.audio.path
                command = 'ffmpeg -i '+location+' -c:a aac -b:a 128k -vn -hls_time 10 -hls_list_size 0 '+location.replace('.mp3', '')+'.m3u8'
                command = command.split()
                cmd2 = subprocess.Popen(command, stdout=subprocess.PIPE)
                cmd2.wait()
            return JsonResponse({}, status=status.HTTP_200_OK)
                
        else:
            artists = Artist.objects.get(id=artist_id)
            genres = Genre.objects.order_by('name').all()
            albums = Album_Artists.objects.filter(artist_id=artist_id).order_by('order').all()
                
            song = None
            song_genres = []
            if song_id > 0:
                song = Song.objects.get(id=song_id)
                song_genres = list(song.genres.order_by('name').values('id'))
                song_genres = [i['id'] for i in song_genres]
                artists = song.artists.order_by('order')
            
            payload = {
                "artists": artists,
                "artist_id": artist_id,
                "genres": genres,
                "song_id": song_id,
                "song": song,
                "song_genres": song_genres,
                "albums": albums
            }
            return render(request, './dashboard/artists/create-song.html', context=payload)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Artist, Surat, Yyl sayladynmy?"}, status=status.HTTP_409_CONFLICT)

@user_passes_test(lambda u: u.is_superuser)
def album_details(request, artist_id, album_id):
    try:
        countries = Country.objects.all()
        artists = Artist.objects.get(id=artist_id)
        genres = Genre.objects.order_by('name').all()
        
        album = None
        if album_id > 0:
            album = Album.objects.prefetch_related('artists').get(id=album_id)
            artists = album.artists.order_by('order')
        
        payload = {
            "countries": countries,
            "artists": artists,
            "album_id": album_id,
            "album": album,
            "artist_id": artist_id,
            "genres": genres
        }
        return render(request, './dashboard/artists/album-details.html', context=payload)
    except Exception as e:
        print(e)
        return JsonResponse({"message": "Artist, Surat, Yyl sayladynmy?"}, status=status.HTTP_409_CONFLICT)
    
class AlbumArtistsListView(generics.ListAPIView):
    serializer_class = AlbumArtistsListSerializer
    queryset =  Artist.objects.order_by('-id').all()
    pagination_class = None
    permission_classes = [SuperUserOnly]

    def get(self, request, *args, **kwargs):
        search_str = request.GET.get("search_user", None)
        queryset = self.filter_queryset(self.get_queryset())
        
        if search_str:
            queryset = queryset.filter(Q(name__icontains=search_str))
        
        queryset = queryset[:20]
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)