from init_spotipy import spotipy_init
import album_metadata
import random


def add_albums(my_albums, items):
    my_albums.extend(items)


def get_all_albums_from_spotify() -> dict[str, album_metadata.AlbumMetadata]:
    sp = spotipy_init()
    print("Reading all your saved albums from Spotify...")
    my_albums = []
    result = sp.current_user_saved_albums()
    add_albums(my_albums, result['items'])
    while result['next']:
        result = sp.next(result)
        add_albums(my_albums, result['items'])

    albums = {}
    for album in my_albums:
        album_id = album['album']['id']
        artist = album['album']['artists'][0]['name']
        album_name = album['album']['name']
        selected_count = 0
        albums[album_id] = album_metadata.AlbumMetadata(
            album_id, album_name, artist, selected_count)

    return albums


def read_all_albums_from_file(filename: str) -> dict[str, album_metadata.AlbumMetadata]:
    print(f'Reading saved album metadata from file {filename}...')
    albums = album_metadata.AlbumMetadata.read_from_file(
        filename)
    return albums


def write_all_albums_to_file(albums: dict[str, album_metadata.AlbumMetadata], filename: str) -> dict[str, album_metadata.AlbumMetadata]:
    print(f'Writing album metadata from file {filename}...')
    album_metadata.AlbumMetadata.write_to_file(
        albums, filename)
    return albums


def update_albums_selected_counts_in_file(albums: dict[str, album_metadata.AlbumMetadata], filename: str):
    albums_in_file = album_metadata.AlbumMetadata.read_from_file(
        filename)
    for album_id, album in albums.items():
        if album_id in albums_in_file:
            albums_in_file[album_id].selected_count += 1
        else:
            albums_in_file[album_id] = album
    album_metadata.AlbumMetadata.write_to_file(
        albums_in_file, filename)


def filter_albums_with_selected_count(albums: dict[str, album_metadata.AlbumMetadata]) -> dict[str, album_metadata.AlbumMetadata]:
    assert len(albums) >= 10, \
        "There are not enough albums to select 10 random albums from."

    filtered_albums = {}

    # Get the max selected count from albums
    max_selected_count = 0
    for album in albums.values():
        if album.selected_count > max_selected_count:
            max_selected_count = album.selected_count

    # Get the min selected count from albums
    min_selected_count = max_selected_count
    for album in albums.values():
        if album.selected_count < min_selected_count:
            min_selected_count = album.selected_count

    # Filter some albums based on the selected count
    if max_selected_count == min_selected_count:
        filtered_albums = albums
    while len(filtered_albums) < 10:
        for album_id, album in albums.items():
            if album.selected_count == min_selected_count:
                filtered_albums[album_id] = album
        min_selected_count += 1
    return filtered_albums


def select_10_random_albums(albums: dict[str, album_metadata.AlbumMetadata]) -> dict[str, album_metadata.AlbumMetadata]:
    assert len(albums) >= 10, \
        "There are not enough albums to select 10 random albums from."

    filtered_albums = filter_albums_with_selected_count(albums)

    # Randomly select 10 albums from the filtered albums
    random_albums = {}
    while len(random_albums) < 10:
        random_album_id = random.choice(list(filtered_albums.keys()))
        random_album = filtered_albums.pop(random_album_id)
        random_albums.update({random_album_id: random_album})
    return random_albums
