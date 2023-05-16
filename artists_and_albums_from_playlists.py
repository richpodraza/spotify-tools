from init_spotipy import spotipy_init
from spotipy.oauth2 import SpotifyOAuth


def get_artists_and_albums_from_playlists(sp, playlists, user, artists, albums):
    for playlist in playlists["items"]:
        if playlist["owner"]["id"] == user["id"]:
            # print(playlist['name'])
            tracks = sp.playlist_tracks(playlist["id"])
            add_artists_and_albums_from_tracks(tracks, artists, albums)
            while tracks["next"]:
                tracks = sp.next(tracks)
                add_artists_and_albums_from_tracks(tracks, artists, albums)


def add_or_increment_count(map, key):
    if key in map:
        map.update({key: map[key] + 1})
    else:
        map.update({key: 1})


def add_artists_and_albums_from_tracks(tracks, artists, albums):
    for item in tracks["items"]:
        add_or_increment_count(
            albums, (item["track"]["album"]["name"], item["track"]["album"]["id"])
        )
        for artist in item["track"]["artists"]:
            add_or_increment_count(artists, (artist["name"], artist["id"]))


def follow_artists_and_albums_from_playlists():
    sp = spotipy_init()
    user = sp.current_user()

    artists = dict()
    albums = dict()

    # Print artists and albums from playlists
    playlists = sp.current_user_playlists()

    get_artists_and_albums_from_playlists(sp, playlists, user, artists, albums)
    while playlists["next"]:
        playlists = sp.next(playlists)
        get_artists_and_albums_from_playlists(sp, playlists, user, artists, albums)

    print(len(albums.keys()), len(artists.keys()))

    # filter out albums or artists with less than 5 tracks counted
    for album, track_count in albums.items():
        # if track_count > 3:
        print(album[0], album[1], track_count, sep="\t")

    for artist, track_count in artists.items():
        # if track_count > 3:
        print(artist[0], artist[1], track_count, sep="\t")

    # Go through and follow artists or albums with more than X count
    albums_to_save = []
    for album, track_count in albums.items():
        if track_count >= 3:
            albums_to_save.append(album[1])

    artists_to_follow = []
    for artist, track_count in artists.items():
        if track_count >= 5:
            artists_to_follow.append(artist[1])

    # To avoid 414 error, need to limit this list, try 50 at a time
    i = 0
    while i < len(artists_to_follow):
        j = i + 50
        if j > len(artists_to_follow):
            j = len(artists_to_follow)
        print(f"Following artists between {i} and {j}")
        sp.user_follow_artists(artists_to_follow[i:j])
        i = j


if __name__ == "__main__":
    follow_artists_and_albums_from_playlists()
