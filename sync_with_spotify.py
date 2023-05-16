import get_all_albums


def sync_with_spotify():
    '''
    If I've added new albums on Spotify, add them to the local file.
    If I've removed albums from Spotify, just ignore that for now.
    '''
    filename = 'album_metadata.json'
    albums_from_spotify = get_all_albums.get_all_albums_from_spotify()
    albums_from_file = get_all_albums.read_all_albums_from_file(filename)
    for album_id, album in albums_from_spotify.items():
        if album_id not in albums_from_file:
            print(f'Adding album {album.album_name} by {album.artist}...')
            albums_from_file[album_id] = album
    get_all_albums.write_all_albums_to_file(albums_from_file, filename)


if __name__ == '__main__':
    sync_with_spotify()
