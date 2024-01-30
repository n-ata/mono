from django.urls import path, re_path
from django.contrib.auth import views as auth_views

from .views import (
    artists,
    ArtistsListView,
    create_artist,
    artist_details,
    delete_artists,
    ArtistSongsListView,
    edit_artist,
    create_album,
    AlbumArtistsListView,
    album_details,
    AlbumSongsListView,
    delete_songs,
    delete_albums,
    create_album_song,
    create_song
    
)

urlpatterns = [
    # begin auth
    path('login/',auth_views.LoginView.as_view(template_name='dashboard/authentication/login.html', redirect_authenticated_user=True),name='sign_in'),
    path('logout/',auth_views.LogoutView.as_view(template_name='dashboard/authentication/logout.html'),name='logout'),
    # end auth

    path('', artists, name='home'),
    
    # begin artists
    path('artists', artists, name='artists'),
    path('artists-list', ArtistsListView.as_view(), name='ArtistsListView'),
    path('create-artist', create_artist, name='create-artist'),
    path('edit-artist/<int:id>', edit_artist, name='edit-artist'),
    path('delete-artists',delete_artists, name='delete-artists'),
    path('artist-details/<int:id>', artist_details, name='artist-details'),
    path('artist-songs-list/<int:id>', ArtistSongsListView.as_view(), name='ArtistSongsListView'),
    
    path('delete-songs', delete_songs, name='delete-songs'),
    
    path('delete-albums', delete_albums, name='delete-albums'),
    
    
    path('album-songs-list/<int:id>', AlbumSongsListView.as_view(), name='AlbumSongsListView'),
    
    path('create-album/<int:artist_id>/<int:album_id>', create_album, name='create-album'),
    path('create-album-song/<int:artist_id>/<int:album_id>/<int:song_id>', create_album_song, name='create-album-song'),
    path('create-song/<int:artist_id>/<int:song_id>', create_song, name='create-song'),
    path('album-details/<int:artist_id>/<int:album_id>', album_details, name='album-details'),
    path('album-artists-list', AlbumArtistsListView.as_view(), name='AlbumArtistsListView'),
    
]
